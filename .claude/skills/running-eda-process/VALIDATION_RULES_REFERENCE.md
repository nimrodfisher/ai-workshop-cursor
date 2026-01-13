# Validation Rules Reference

This document provides detailed validation rules to apply during the EDA process. Referenced from SKILL.md when detailed validation logic is needed.

## Join Validation (Detailed Rules)

### 1.1 Row Count Impact Analysis

**When to run:** Before and after every JOIN operation

**SQL Pattern:**
```sql
-- Step 1: Count left table
SELECT COUNT(*) as left_count FROM left_table;

-- Step 2: Count result after join
SELECT COUNT(*) as result_count 
FROM left_table l
LEFT JOIN right_table r ON l.key = r.key;

-- Step 3: Calculate impact
-- Fan-out: result_count > left_count (multiple matches on right)
-- Data loss: result_count < left_count (inner join or filtering)
```

**Severity Thresholds:**
- Change >5%: ⚠️ WARNING (investigate)
- Change >20%: 🚨 FAIL (likely data issue)

**Example Report:**
```
✓ CHECK: Row Count Impact (users → orders join)
  What: Measuring join multiplier effect
  Result: ⚠️ WARNING
  Details:
    - Left table (users): 10,000 rows
    - After join: 10,847 rows
    - Fan-out: +8.5% (847 extra rows)
    - Cause: 847 users have multiple orders
    - Expected: Yes (1:many relationship)
```

### 1.2 Orphan Record Detection

**When to run:** Every LEFT JOIN operation

**SQL Pattern:**
```sql
SELECT 
    COUNT(*) as total_left,
    COUNT(r.key) as matched,
    COUNT(*) - COUNT(r.key) as orphans,
    ROUND(100.0 * (COUNT(*) - COUNT(r.key)) / COUNT(*), 2) as orphan_pct
FROM left_table l
LEFT JOIN right_table r ON l.key = r.key;
```

**Severity Thresholds:**
- Orphans <5%: ✓ PASS
- Orphans 5-10%: ⚠️ WARNING
- Orphans >10%: 🚨 FAIL (unless expected)

**Example Report:**
```
✓ CHECK: Orphan Records (subscriptions → customers)
  What: Identifying subscriptions without customer records
  Result: 🚨 FAIL
  Details:
    - Total subscriptions: 5,000
    - Matched to customers: 4,766 (95.3%)
    - Orphaned: 234 (4.7%)
    - Action Required: Investigate 234 orphaned subscriptions
```

### 1.3 Duplicate Key Detection

**When to run:** Before joining, especially on the "one" side of 1:many

**SQL Pattern:**
```sql
-- Check for duplicates on join key
SELECT 
    key,
    COUNT(*) as occurrences
FROM table_name
GROUP BY key
HAVING COUNT(*) > 1
ORDER BY occurrences DESC
LIMIT 10;
```

**Severity Logic:**
- No duplicates on "one" side: ✓ PASS
- Duplicates on "one" side: 🚨 FAIL (causes unexpected fan-out)
- Expected duplicates on "many" side: ✓ PASS

## Aggregation Validation (Detailed Rules)

### 2.1 Percentage Sum Validation

**When to run:** Any query producing percentage columns

**SQL Pattern:**
```sql
-- After aggregation
SELECT 
    SUM(percentage_column) as total_pct
FROM aggregation_result;

-- Should equal 100.0 (±0.1 tolerance for rounding)
```

**Severity Thresholds:**
- 99.9-100.1%: ✓ PASS
- 99.0-99.9% or 100.1-101.0%: ⚠️ WARNING (rounding issues)
- <99% or >101%: 🚨 FAIL (calculation error)

### 2.2 Segment Total Reconciliation

**When to run:** Any GROUP BY operation

**SQL Pattern:**
```sql
-- Compare source count to aggregated count
WITH source_count AS (
    SELECT COUNT(*) as source_total
    FROM source_table
),
segment_count AS (
    SELECT SUM(count_column) as segment_total
    FROM aggregation_result
)
SELECT 
    source_total,
    segment_total,
    source_total - segment_total as difference
FROM source_count, segment_count;
```

**Severity Logic:**
- Difference = 0: ✓ PASS
- Difference > 0: 🚨 FAIL (records missing from segments)

### 2.3 Logical Value Range Checks

**When to run:** After calculating any business metrics

**Validation Rules:**
- Counts: Must be ≥ 0 (no negative counts)
- Revenue: Usually ≥ 0 (unless refunds included)
- Rates/Percentages: Must be 0-100%
- Dates: Must be ≤ current_date (no future dates)

**SQL Pattern:**
```sql
-- Check for impossible values
SELECT 
    COUNT(*) as invalid_records
FROM result_table
WHERE 
    count_column < 0
    OR rate_column < 0
    OR rate_column > 100
    OR date_column > CURRENT_DATE;
```

### 2.4 Concentration Detection

**When to run:** Segmentation or categorical aggregations

**SQL Pattern:**
```sql
-- Find top segment concentration
WITH totals AS (
    SELECT SUM(metric) as total FROM result_table
)
SELECT 
    category,
    metric,
    ROUND(100.0 * metric / total, 2) as pct_of_total
FROM result_table, totals
ORDER BY pct_of_total DESC
LIMIT 1;
```

**Severity Thresholds:**
- Max segment <90%: ✓ PASS (healthy distribution)
- Max segment ≥90%: ⚠️ WARNING (extreme concentration)

## Segment/Cohort Validation (Detailed Rules)

### 3.1 Mutual Exclusivity Check

**When to run:** Creating user segments or cohorts

**SQL Pattern:**
```sql
-- Check for entities in multiple segments
SELECT 
    entity_id,
    COUNT(DISTINCT segment) as segment_count
FROM segment_assignments
GROUP BY entity_id
HAVING COUNT(DISTINCT segment) > 1;
```

**Severity Logic:**
- 0 overlaps: ✓ PASS (perfectly exclusive)
- Any overlaps: 🚨 FAIL (unless overlapping segments are expected)

### 3.2 Complete Coverage Validation

**When to run:** After segmentation

**SQL Pattern:**
```sql
-- Compare source entities to segmented entities
WITH source AS (
    SELECT COUNT(DISTINCT entity_id) as total FROM source_table
),
segmented AS (
    SELECT COUNT(DISTINCT entity_id) as covered FROM segment_table
)
SELECT 
    total,
    covered,
    total - covered as uncovered,
    ROUND(100.0 * covered / total, 2) as coverage_pct
FROM source, segmented;
```

**Severity Thresholds:**
- 100% coverage: ✓ PASS
- 95-99.9% coverage: ⚠️ WARNING (document uncovered)
- <95% coverage: 🚨 FAIL (incomplete segmentation)

### 3.3 NULL/Unknown Bucket Size

**When to run:** Categorical aggregations with NULL handling

**SQL Pattern:**
```sql
-- Measure NULL or "Unknown" segment size
SELECT 
    CASE 
        WHEN category IS NULL THEN 'NULL/Unknown'
        ELSE category 
    END as category,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as pct
FROM source_table
GROUP BY category
ORDER BY count DESC;
```

**Severity Thresholds:**
- NULL bucket <5%: ✓ PASS
- NULL bucket 5-20%: ⚠️ WARNING (acceptable)
- NULL bucket >20%: 🚨 FAIL (data quality issue)

### 3.4 Statistical Significance Check

**When to run:** Before comparing segments

**Minimum Sample Size Rules:**
- Segment size ≥30: Acceptable for basic analysis
- Segment size ≥100: Better for ratio comparisons
- Segment size ≥1000: Reliable for detailed analysis

**SQL Pattern:**
```sql
-- Find undersized segments
SELECT 
    segment,
    COUNT(*) as size,
    CASE 
        WHEN COUNT(*) < 30 THEN 'Too Small'
        WHEN COUNT(*) < 100 THEN 'Marginal'
        ELSE 'Sufficient'
    END as statistical_adequacy
FROM segment_table
GROUP BY segment
HAVING COUNT(*) < 100
ORDER BY size;
```

## Time-Series Validation (Detailed Rules)

### 4.1 Date Continuity Check

**When to run:** Any temporal analysis

**SQL Pattern:**
```sql
-- Find gaps in date sequence
WITH date_range AS (
    SELECT 
        MIN(date_column) as start_date,
        MAX(date_column) as end_date,
        COUNT(DISTINCT date_column) as actual_days
    FROM source_table
),
expected AS (
    SELECT 
        start_date,
        end_date,
        DATEDIFF(day, start_date, end_date) + 1 as expected_days
    FROM date_range
)
SELECT 
    start_date,
    end_date,
    expected_days,
    actual_days,
    expected_days - actual_days as missing_days
FROM expected, date_range;
```

**Severity Logic:**
- 0 missing days: ✓ PASS (complete)
- Missing days documented: ⚠️ WARNING (e.g., weekends, holidays)
- Unexplained gaps: 🚨 FAIL (investigate)

### 4.2 Future Date Detection

**When to run:** Every date-based query

**SQL Pattern:**
```sql
-- Find future dates
SELECT 
    COUNT(*) as future_records,
    MAX(date_column) as latest_date,
    CURRENT_DATE as today
FROM source_table
WHERE date_column > CURRENT_DATE;
```

**Severity Logic:**
- 0 future dates: ✓ PASS
- Any future dates: 🚨 FAIL (data quality issue)

### 4.3 Volatility Detection

**When to run:** Time-series trend analysis

**SQL Pattern:**
```sql
-- Calculate period-over-period change
WITH metrics AS (
    SELECT 
        period,
        metric,
        LAG(metric) OVER (ORDER BY period) as prev_metric
    FROM period_table
)
SELECT 
    period,
    metric,
    prev_metric,
    ROUND(100.0 * (metric - prev_metric) / NULLIF(prev_metric, 0), 2) as pct_change
FROM metrics
WHERE ABS(100.0 * (metric - prev_metric) / NULLIF(prev_metric, 0)) > 50
ORDER BY ABS(pct_change) DESC;
```

**Severity Thresholds:**
- Change <30%: ✓ PASS (normal fluctuation)
- Change 30-50%: ⚠️ WARNING (notable change)
- Change >50%: 🚨 FAIL (investigate immediately)

### 4.4 Consistent Granularity Check

**When to run:** Comparing periods in time-series

**SQL Pattern:**
```sql
-- Check record count consistency across periods
WITH period_counts AS (
    SELECT 
        period,
        COUNT(*) as record_count
    FROM source_table
    GROUP BY period
),
stats AS (
    SELECT 
        AVG(record_count) as avg_count,
        STDDEV(record_count) as std_count
    FROM period_counts
)
SELECT 
    p.period,
    p.record_count,
    s.avg_count,
    ROUND(100.0 * p.record_count / s.avg_count, 2) as pct_of_avg
FROM period_counts p, stats s
WHERE p.record_count < 0.5 * s.avg_count
ORDER BY pct_of_avg;
```

**Severity Thresholds:**
- All periods within 50% of average: ✓ PASS
- Some periods <50% of average: ⚠️ WARNING (investigate)

## Final Output Validation (Detailed Rules)

### 5.1 Business Question Alignment

**Checklist:**
- [ ] Does output answer the original question?
- [ ] Are all requested metrics present?
- [ ] Are all requested dimensions included?
- [ ] Is the time period correct?
- [ ] Are filters applied as requested?

### 5.2 Column Naming Standards

**Rules:**
- Use business-friendly names (not technical)
- No raw IDs in final output (unless specifically requested)
- Clear units (e.g., "revenue_usd" not "revenue")
- Consistent naming (e.g., "user_count" not mix of "users" and "customer_count")

**Examples:**
- ✅ Good: `monthly_revenue_usd`, `customer_count`, `avg_order_value`
- ❌ Bad: `rev`, `cnt`, `col_3`

### 5.3 Sensitive Data Check

**Scan for:**
- Personal Identifiable Information (PII): emails, phone numbers, full names
- Internal IDs that shouldn't be exposed
- Confidential metrics (if sharing externally)

**SQL Pattern:**
```sql
-- Check column names for PII indicators
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'result_table'
  AND (
    column_name LIKE '%email%'
    OR column_name LIKE '%phone%'
    OR column_name LIKE '%ssn%'
    OR column_name LIKE '%address%'
  );
```

### 5.4 Edge Case Documentation

**Document:**
- Records excluded (and why)
- Filters applied
- Data quality caveats
- Time period limitations
- Known data issues

**Template:**
```
DATA NOTES:
- Excluded: Trial accounts (12% of total)
- Filter: Active subscriptions only (status = 'active')
- Period: June 2024 - December 2024 (6 months)
- Caveat: October data incomplete due to system migration
```

## Quick Reference: Validation Decision Tree

```
Start Analysis
    ↓
Load schema.yml from GitHub?
    No → STOP (mandatory first step)
    Yes ↓
Run Sanity Checks?
    No → STOP (mandatory phase 1)
    Yes ↓
Run EDA?
    No → STOP (mandatory phase 2)
    Yes ↓
Any 🚨 FAIL results?
    Yes → STOP (fix issues first)
    No ↓
Any ⚠️ WARNING results?
    Yes → Document & explain
    ↓
Present Checkpoint 1?
    No → STOP (mandatory checkpoint)
    Yes ↓
User approved?
    No → PAUSE (wait for guidance)
    Yes ↓
Proceed to Main Analysis ✅
```







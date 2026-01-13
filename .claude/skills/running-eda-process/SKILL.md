---
name: running-eda-process
description: Runs Exploratory Data Analysis (EDA) following the mandatory validation workflow. Use when performing data analysis, exploring datasets, validating data quality, or when the user mentions EDA, data exploration, sanity checks, or data validation. Always run before main analysis queries.
version: 1.0.0
author: Nimrod Fisher | AI Analytics Hub
tags: eda, data-validation, exploratory-analysis, sanity-checks, data-quality
---

# Running EDA Process

This Skill guides you through the mandatory Exploratory Data Analysis (EDA) workflow, ensuring data quality is validated before any analysis begins.

## Critical Rules

**⚠️ MANDATORY WORKFLOW ORDER:**

```
Phase 0: Load schema.yml from GitHub (ALWAYS FIRST)
    ↓
Phase 1: Run Sanity Checks on all relevant tables
    ↓
Phase 2: Run EDA on all relevant tables
    ↓
🛑 CHECKPOINT 1: Present validation results, ask permission to proceed
```

**🚫 NEVER skip Phases 0, 1, or 2 before writing main analysis queries**

## Phase 0: Load Schema Context (MANDATORY FIRST STEP)

Before any analysis begins, you MUST load the schema.yml file from GitHub.

### Instructions

1. **Use GitHub MCP tool** to fetch schema:

```
Tool: mcp_github_get_file_contents
Parameters:
  - owner: "nimrodfisher"
  - repo: "workshop-queries-repo"
  - path: "schema.yml"
```

2. **What schema.yml provides:**
   - Table definitions and column meanings
   - Standard metric calculations (MRR, Churn, ARPU, etc.)
   - Pre-built query patterns for common questions
   - Table relationships and join patterns
   - SQL formatting standards

3. **Reference schema throughout analysis:**
   - Use `common_metrics` for metric definitions
   - Use `models` for table/column descriptions
   - Use `relationships` for joins
   - Use `common_business_questions` for query patterns

**This step is NON-NEGOTIABLE. No analysis starts without schema.yml loaded.**

## Phase 1: Sanity Checks

Run data quality checks on all relevant tables BEFORE exploring the data.

### What to Check

Execute `framework.run_sanity_checks("table_name")` which validates:

1. **Basic Statistics:**
   - Row counts
   - Null counts per column
   - Unique value counts
   - Data type consistency

2. **Data Quality:**
   - Missing values (>20% nulls flag warning)
   - Duplicate records
   - Invalid values (negatives where shouldn't be)
   - Future dates
   - Orphaned foreign keys

3. **Business Logic:**
   - Expected value ranges
   - Required fields populated
   - Valid enum values

### Reporting Format

Use this format for every check:

```
✓ CHECK: [Test Name]
  What: [Brief description of what's being tested]
  Result: [PASS / ⚠️ WARNING / 🚨 FAIL]
  Details: [Numbers or explanation]
```

**Example:**

```
✓ CHECK: Null Value Scan (users table)
  What: Identifying columns with excessive missing data
  Result: ⚠️ WARNING
  Details:
    - email: 0% nulls (good)
    - phone: 23% nulls (flag for investigation)
    - created_at: 0% nulls (good)
```

### When to Flag Issues

| Severity | When | Action |
|----------|------|--------|
| 🚨 FAIL | Data corruption, logical impossibilities | STOP - Fix before continuing |
| ⚠️ WARNING | Unexpected patterns, high nulls | Document and proceed with caution |
| ✓ PASS | All checks within expected ranges | Continue to next phase |

## Phase 2: Exploratory Data Analysis (EDA)

After sanity checks pass, explore data distributions and patterns.

### What to Analyze

Execute `framework.run_eda("table_name", sample_size=1000)` which provides:

1. **Distribution Analysis:**
   - Numeric columns: min, max, mean, median, std dev, quartiles
   - Categorical columns: value counts, cardinality, top values
   - Date columns: range, gaps, temporal patterns

2. **Pattern Detection:**
   - Outliers (values beyond 3 standard deviations)
   - Skewness and kurtosis
   - Concentration (single value dominating >90%)
   - Correlation between key fields

3. **Business Context:**
   - Data recency (latest record date)
   - Completeness (% of expected records present)
   - Segment balance (distribution across categories)

### EDA Output Structure

For each table, document:

```
═══════════════════════════════════════════════════════
📊 EDA REPORT: [table_name]
═══════════════════════════════════════════════════════
Rows Analyzed: X,XXX

NUMERIC COLUMNS:
  • [column_name]
    Range: [min] to [max]
    Mean: [value] | Median: [value]
    Std Dev: [value]
    Outliers: [count] records ([%])
    Key Insight: [1 sentence]

CATEGORICAL COLUMNS:
  • [column_name]
    Unique Values: [count]
    Top Value: "[value]" ([X]% of records)
    Distribution: [Balanced / Concentrated / Skewed]
    Key Insight: [1 sentence]

DATE COLUMNS:
  • [column_name]
    Range: [earliest] to [latest]
    Gaps: [count] missing periods
    Recency: [description]
    Key Insight: [1 sentence]

═══════════════════════════════════════════════════════
```

### Key Metrics to Calculate

Always include these in EDA:

- **Cardinality**: Count distinct values
- **Coverage**: % non-null values
- **Concentration**: % held by top value
- **Recency**: Days since latest record
- **Completeness**: % of expected records present

## Data Validation Rules

### Join Validation

When analyzing joins between tables, check:

1. **Row Count Impact:**
   ```sql
   -- Before join: COUNT(*) from left table
   -- After join: COUNT(*) from result
   -- Flag if: increase >5% (fan-out) or decrease >5% (data loss)
   ```

2. **Orphan Records:**
   ```sql
   -- Count records from LEFT JOIN where right side is NULL
   -- Flag if: >10% orphans (unless expected)
   ```

3. **Duplicate Keys:**
   ```sql
   -- Check join keys for duplicates before joining
   -- Flag if: duplicates exist on "one" side of 1:many join
   ```

### Aggregation Sanity

After GROUP BY operations, validate:

1. **Percentage Sum:** Should equal ~100% (tolerance ±1%)
2. **Segment Totals:** Must match source record count
3. **Value Ranges:** No negative counts, rates within 0-100%
4. **Concentration:** No single segment >90% (unless expected)

### Time-Series Validation

For temporal analysis, check:

1. **Date Continuity:** No unexpected gaps
2. **No Future Dates:** All dates ≤ current_date
3. **Volatility:** Flag >50% period-over-period changes
4. **Consistent Granularity:** Similar record counts per period

## CHECKPOINT 1: Validation Summary (MANDATORY)

After completing Phases 1 and 2, you MUST present this summary and wait for approval:

```
---
CHECKPOINT 1: Validation & EDA Complete - Ready for Analysis
---
What I just did:
- Loaded schema.yml from GitHub for business context
- Completed sanity checks on [table names]: [X passed, Y warnings, Z failures]
- Completed EDA on [table names]: [key distributions, patterns found]
- Validated data quality: [overall quality score/assessment]

Key findings from validation:
- [Finding 1 - e.g., "monthly_price ranges from $10-$500, no nulls"]
- [Finding 2 - e.g., "Date range: June 2024 to Dec 2025, complete"]
- [Finding 3 - e.g., "3 plan tiers: Enterprise (30%), Free (35%), Pro (35%)"]

Data quality: [READY / NEEDS ATTENTION]

Next steps:
- Write and execute main analysis queries to answer business questions
- Apply insights from EDA to guide query construction
- Generate findings and synthesize results
- Save all query results to data/ folder in JSON format

Should I proceed with writing the main analysis queries?
```

**⚠️ WAIT for user response before continuing to main analysis.**

User may respond:
- "Yes" / "Proceed" → Continue to Phase 3 (Main Analysis)
- "No" / "Stop" → Pause, await further instructions
- "Skip checkpoints" → Set SKIP_CHECKPOINTS = True, continue without pausing

## Best Practices

### 1. Always Explain What You're Checking

❌ Bad: "Running validation checks..."

✅ Good: "Checking user_id uniqueness in the users table to ensure no duplicate accounts exist before analyzing signup trends."

### 2. Show Actual Numbers

❌ Bad: "Result: PASS"

✅ Good: "Result: PASS - 10,000 rows analyzed, 0 duplicates found, all IDs unique"

### 3. Flag Issues Early

If you find a 🚨 FAIL during sanity checks:
1. **STOP immediately**
2. **Explain the issue** in business terms
3. **Ask user how to proceed** (fix data, exclude records, adjust analysis scope)

### 4. Document Assumptions

Always state:
- What filters were applied
- What records were excluded (and why)
- What time periods were analyzed
- What business logic was applied

### 5. Save EDA Results

Store EDA outputs in structured format:

```python
# Save to eda/ folder
eda_report = {
    "table": "users",
    "analyzed_at": "2024-12-15T10:30:00Z",
    "row_count": 10000,
    "columns": {...},
    "quality_score": "READY"
}

with open("eda/eda_report.json", "w") as f:
    json.dump(eda_report, f, indent=2)
```

## Common EDA Patterns

### Pattern 1: New Dataset Exploration

When first encountering a dataset:

1. Load schema.yml for context
2. Run sanity checks on all tables
3. Run EDA on primary table
4. Identify key dimensions and metrics
5. Check data recency and completeness
6. Present Checkpoint 1

### Pattern 2: Multi-Table Analysis

When analyzing joins:

1. Load schema.yml (relationships section)
2. Run sanity checks on each table
3. Run EDA on each table
4. Validate join keys (uniqueness, coverage)
5. Test join with small sample
6. Validate row count impact
7. Present Checkpoint 1

### Pattern 3: Time-Series Investigation

When analyzing trends:

1. Load schema.yml (date column meanings)
2. Run sanity checks (date validity)
3. Run EDA with date distribution focus
4. Check for gaps in time periods
5. Validate volatility patterns
6. Present Checkpoint 1

## Troubleshooting

### "Skip EDA for quick analysis"

**Never skip EDA.** Even for "quick" analyses:
- Bad data → bad insights → bad decisions
- 5 minutes of validation saves hours of rework
- Always follow the mandatory workflow order

### "Data looks fine to me"

Your intuition isn't enough:
- Always run automated checks
- Always document what was validated
- Always show the actual numbers
- Surprises hide in the details

### "Can I run EDA and analysis together?"

No. The workflow is sequential for good reason:
1. Schema context informs what to validate
2. Sanity checks catch data corruption early
3. EDA reveals patterns that guide analysis design
4. Checkpoint 1 ensures alignment before heavy lifting

## Integration with Analysis Workflow

EDA is **Phase 2** of the complete workflow:

```
Phase 0: Load schema.yml ✅
Phase 1: Sanity Checks ✅
Phase 2: EDA ✅ [YOU ARE HERE]
Phase 3: Main Analysis (after Checkpoint 1 approval)
Phase 4: Synthesis
Phase 5: Report Generation
Phase 6: Documentation
```

After Checkpoint 1 approval, you'll proceed to:
- Write main analysis queries (using schema.yml context)
- Execute queries with validation enabled
- Save results to data/ folder
- Present Checkpoint 2 after first query execution

## Quick Reference Card

```
┌─────────────────────────────────────────┐
│ EDA PROCESS QUICK REFERENCE             │
├─────────────────────────────────────────┤
│ Phase 0: Load schema.yml (GitHub MCP)   │
│ Phase 1: Sanity checks (all tables)     │
│ Phase 2: EDA (distributions, patterns)  │
│ Phase 3: Present Checkpoint 1 & WAIT    │
├─────────────────────────────────────────┤
│ Check Format:                           │
│   ✓ CHECK: [Name]                       │
│   What: [Description]                   │
│   Result: [PASS/WARNING/FAIL]           │
│   Details: [Numbers]                    │
├─────────────────────────────────────────┤
│ Severity Levels:                        │
│   🚨 FAIL → Stop immediately            │
│   ⚠️ WARNING → Document & proceed       │
│   ✓ PASS → Continue                     │
└─────────────────────────────────────────┘
```

## Examples

### Example 1: Basic EDA Workflow

**User Request:** "Analyze user signups by month"

**EDA Process:**

```python
# Phase 0: Load schema.yml
# (Use GitHub MCP tool as shown above)

# Phase 1: Sanity Checks
framework.run_sanity_checks("users")

# Output:
# ✓ CHECK: Row Count
#   What: Verifying table is not empty
#   Result: PASS
#   Details: 10,000 users found
#
# ✓ CHECK: Null Value Scan
#   What: Checking for missing critical data
#   Result: PASS
#   Details: All required fields populated (email, created_at)

# Phase 2: EDA
framework.run_eda("users", sample_size=1000)

# Output:
# 📊 EDA REPORT: users
# NUMERIC COLUMNS:
#   • user_id: Range 1 to 10,000 (sequential, no gaps)
#
# DATE COLUMNS:
#   • created_at: 
#     Range: 2024-01-01 to 2024-12-15
#     Gaps: None detected
#     Recency: Current (last signup today)

# Phase 3: Present Checkpoint 1
# (Show summary and wait for approval)
```

### Example 2: Multi-Table Analysis

**User Request:** "Calculate revenue by customer tier"

**EDA Process:**

```python
# Phase 0: Load schema.yml
# (Includes table relationships)

# Phase 1: Sanity Checks (multiple tables)
framework.run_sanity_checks("customers")
framework.run_sanity_checks("subscriptions")

# Phase 2: EDA (multiple tables)
framework.run_eda("customers")
framework.run_eda("subscriptions")

# Additional Join Validation:
# ✓ CHECK: Join Key Coverage
#   What: Verifying all subscriptions link to customers
#   Result: ⚠️ WARNING
#   Details: 234 subscriptions (2%) have no matching customer
#   Action: Exclude orphaned records from analysis

# Phase 3: Present Checkpoint 1
# (Include join validation findings)
```

## Related Skills

- **SQL Query Standards**: Use with this Skill for properly formatted queries
- **Report Generation**: Comes after EDA and main analysis
- **Data Validation**: Detailed rules applied during Phases 1 & 2

## References

- Official Claude Skills docs: https://code.claude.com/docs/en/skills
- Project rules: `.cursor/rules/data_validation_master.mdc`
- Agent workflow: `agent_instructions.md`
- Schema context: Load from GitHub (workshop-queries-repo/schema.yml)







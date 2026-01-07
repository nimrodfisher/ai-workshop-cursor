# EDA Process Examples

This document provides complete, end-to-end examples of the EDA process for common analysis scenarios.

## Example 1: Single Table Analysis - User Signups

### Scenario
Analyze monthly user signup trends for the past 6 months.

### Phase 0: Load Schema Context

```python
# Use GitHub MCP tool
mcp_github_get_file_contents(
    owner="nimrodfisher",
    repo="workshop-queries-repo",
    path="schema.yml"
)

# Schema provides context:
# - users table: contains user_id, email, created_at, signup_source
# - created_at: timestamp when user account was created
# - Business question pattern: "Signup trends over time"
```

### Phase 1: Sanity Checks

```python
framework.run_sanity_checks("users")
```

**Output:**

```
═══════════════════════════════════════════════════════
📋 SANITY CHECK REPORT: users
═══════════════════════════════════════════════════════

✓ CHECK: Table Existence
  What: Verifying users table is accessible
  Result: PASS
  Details: Table exists with 15,234 rows

✓ CHECK: Row Count
  What: Checking for minimum data volume
  Result: PASS
  Details: 15,234 users (sufficient for analysis)

✓ CHECK: Null Value Scan
  What: Identifying missing critical data
  Result: PASS
  Details:
    - user_id: 0% nulls ✓
    - email: 0.2% nulls (34 users) ⚠️
    - created_at: 0% nulls ✓
    - signup_source: 12% nulls (1,828 users) ⚠️

✓ CHECK: Date Validity
  What: Checking created_at for impossible dates
  Result: PASS
  Details:
    - Date range: 2023-01-15 to 2024-12-15
    - No future dates found
    - No NULL dates

✓ CHECK: Duplicate Detection
  What: Looking for duplicate user_id values
  Result: PASS
  Details: All 15,234 user_ids are unique

═══════════════════════════════════════════════════════
Summary: 5 checks performed
├── Passed: 5
├── Warnings: 2 (documented below)
└── Failed: 0

⚠️ WARNINGS TO NOTE:
1. email: 34 users (0.2%) have NULL emails - likely social auth users
2. signup_source: 1,828 users (12%) have NULL source - legacy data before tracking

Overall Status: READY FOR USE
═══════════════════════════════════════════════════════
```

### Phase 2: EDA

```python
framework.run_eda("users", sample_size=1000)
```

**Output:**

```
═══════════════════════════════════════════════════════
📊 EDA REPORT: users
═══════════════════════════════════════════════════════
Rows Analyzed: 15,234
Sample Size: 1,000 (for distribution analysis)

NUMERIC COLUMNS:
  • user_id
    Range: 1 to 15,234 (sequential)
    Distribution: Uniform (as expected for auto-increment)
    Key Insight: No gaps in ID sequence

CATEGORICAL COLUMNS:
  • signup_source
    Unique Values: 4 (Google, Facebook, Email, NULL)
    Distribution:
      - Email: 7,842 (51.5%)
      - Google: 4,123 (27.1%)
      - Facebook: 1,441 (9.5%)
      - NULL: 1,828 (12.0%)
    Concentration: Email dominant but not extreme
    Key Insight: Email signup is most common, NULL bucket is legacy data

  • email_domain (derived)
    Top 10 Domains:
      - gmail.com: 4,521 (29.7%)
      - yahoo.com: 1,234 (8.1%)
      - outlook.com: 876 (5.7%)
    Key Insight: Consumer email providers dominate

DATE COLUMNS:
  • created_at
    Range: 2023-01-15 to 2024-12-15 (23 months)
    Gaps: None detected (daily signups present)
    Recency: Current (last signup today at 10:23 AM)
    Pattern: ~20 signups/day average, weekends slightly lower
    Key Insight: Consistent signup rate, healthy growth

TIME PATTERNS:
  • Signup velocity (last 6 months):
    - June 2024: 612 signups
    - July 2024: 645 signups (+5.4%)
    - August 2024: 701 signups (+8.7%)
    - September 2024: 678 signups (-3.3%)
    - October 2024: 734 signups (+8.3%)
    - November 2024: 698 signups (-4.9%)
    Average: 678 signups/month
    Trend: Slight upward trajectory

DATA QUALITY:
  • Completeness: 99.8% (all required fields populated)
  • Recency: Excellent (data current as of today)
  • Coverage: 6-month analysis period well-represented

═══════════════════════════════════════════════════════
```

### Phase 3: Present Checkpoint 1

```
---
CHECKPOINT 1: Validation & EDA Complete - Ready for Analysis
---
What I just did:
- Loaded schema.yml from GitHub (users table context)
- Completed sanity checks on users table: 5 passed, 2 warnings, 0 failures
- Completed EDA on users table: analyzed 15,234 records covering 23 months
- Identified signup patterns and data quality status

Key findings from validation:
- 15,234 total users from Jan 2023 to Dec 2024
- ~678 signups/month average (last 6 months)
- Email is most common signup source (51.5%)
- 12% of users have NULL signup_source (legacy data, pre-tracking era)
- Data quality is excellent: 99.8% complete, no future dates, no duplicates

Data quality: READY ✅

Next steps:
- Write SQL query to aggregate signups by month
- Apply date filters for last 6 months (June-November 2024)
- Calculate month-over-month growth rates
- Generate trend visualization
- Save results to data/01_monthly_signups.json

Should I proceed with writing the main analysis query?
```

**User responds:** "Yes, proceed"

---

## Example 2: Multi-Table Analysis - Revenue by Customer Tier

### Scenario
Calculate total revenue by customer tier (Free, Pro, Enterprise) for Q4 2024.

### Phase 0: Load Schema Context

```python
# Use GitHub MCP tool
mcp_github_get_file_contents(
    owner="nimrodfisher",
    repo="workshop-queries-repo",
    path="schema.yml"
)

# Schema provides:
# - customers table: customer_id, tier, created_at
# - subscriptions table: subscription_id, customer_id, monthly_price, start_date
# - Relationship: customers 1:many subscriptions
# - Common metric: MRR = SUM(monthly_price) for active subscriptions
```

### Phase 1: Sanity Checks (Multiple Tables)

```python
framework.run_sanity_checks("customers")
framework.run_sanity_checks("subscriptions")
```

**Output:**

```
═══════════════════════════════════════════════════════
📋 SANITY CHECK REPORT: customers
═══════════════════════════════════════════════════════

✓ CHECK: Row Count
  What: Verifying customer table has data
  Result: PASS
  Details: 2,847 customers

✓ CHECK: Null Value Scan
  What: Checking tier classification completeness
  Result: PASS
  Details:
    - customer_id: 0% nulls ✓
    - tier: 0% nulls ✓ (all customers classified)
    - created_at: 0% nulls ✓

✓ CHECK: Tier Distribution
  What: Verifying tier segments are reasonable
  Result: PASS
  Details:
    - Free: 987 (34.7%)
    - Pro: 1,243 (43.7%)
    - Enterprise: 617 (21.7%)
    Distribution is balanced

═══════════════════════════════════════════════════════
📋 SANITY CHECK REPORT: subscriptions
═══════════════════════════════════════════════════════

✓ CHECK: Row Count
  What: Verifying subscription table has data
  Result: PASS
  Details: 3,156 subscriptions

✓ CHECK: Null Value Scan
  What: Checking for missing critical data
  Result: PASS
  Details:
    - subscription_id: 0% nulls ✓
    - customer_id: 0% nulls ✓
    - monthly_price: 0% nulls ✓
    - start_date: 0% nulls ✓

✓ CHECK: Price Validity
  What: Ensuring prices are logical
  Result: PASS
  Details:
    - Range: $0 to $1,200/month
    - All prices >= 0
    - No negative values

✓ CHECK: Foreign Key Integrity
  What: Verifying all subscriptions link to customers
  Result: ⚠️ WARNING
  Details:
    - Total subscriptions: 3,156
    - Matched to customers: 3,142 (99.6%)
    - Orphaned: 14 (0.4%)
    - Action: Exclude 14 orphaned records from analysis

Overall Status: READY (with 1 warning documented)
═══════════════════════════════════════════════════════
```

### Phase 2: EDA (Multiple Tables)

```python
framework.run_eda("customers", sample_size=500)
framework.run_eda("subscriptions", sample_size=500)
```

**Output:**

```
═══════════════════════════════════════════════════════
📊 EDA REPORT: customers
═══════════════════════════════════════════════════════

CATEGORICAL COLUMNS:
  • tier
    Values: Free (987), Pro (1,243), Enterprise (617)
    Distribution: Balanced across tiers
    Key Insight: Pro tier is most popular (43.7%)

DATE COLUMNS:
  • created_at
    Range: 2022-03-10 to 2024-12-15
    Key Insight: Customer base spans ~2.75 years

═══════════════════════════════════════════════════════
📊 EDA REPORT: subscriptions
═══════════════════════════════════════════════════════

NUMERIC COLUMNS:
  • monthly_price
    Range: $0 to $1,200
    Mean: $87.34
    Median: $49.00
    Distribution:
      - $0 (Free tier): 987 subscriptions (31.3%)
      - $49 (Pro tier): 1,243 subscriptions (39.4%)
      - $200-$1,200 (Enterprise): 926 subscriptions (29.3%)
    Key Insight: Clear tier pricing structure

DATE COLUMNS:
  • start_date
    Range: 2022-03-10 to 2024-12-15
    Q4 2024 subscriptions: 742 (23.5% of total)
    Key Insight: Sufficient data for Q4 2024 analysis

JOIN VALIDATION:
  • customers → subscriptions
    Relationship: 1:many
    Coverage: 2,847 customers → 3,142 subscriptions (99.6% match)
    Orphans: 14 subscriptions without customers (0.4%)
    Duplicates: Some customers have multiple subscriptions (expected)
    Key Insight: Join will cause fan-out (expected 1:many behavior)

═══════════════════════════════════════════════════════
```

### Phase 3: Present Checkpoint 1

```
---
CHECKPOINT 1: Validation & EDA Complete - Ready for Analysis
---
What I just did:
- Loaded schema.yml from GitHub (customers + subscriptions context)
- Completed sanity checks on 2 tables: all passed, 1 warning
- Completed EDA on both tables and validated join relationship
- Confirmed Q4 2024 data coverage (742 subscriptions)

Key findings from validation:
- 2,847 customers across 3 tiers (Free: 35%, Pro: 44%, Enterprise: 22%)
- 3,156 total subscriptions (14 orphaned, will exclude)
- Monthly prices range $0-$1,200 (logical for tier structure)
- Q4 2024 has 742 active subscriptions (sufficient for analysis)
- Join will cause expected fan-out (customers can have multiple subscriptions)

Data quality: READY ✅

Next steps:
- Write query to join customers + subscriptions
- Filter for Q4 2024 (Oct-Dec)
- Aggregate revenue by tier
- Calculate tier contributions
- Validate percentages sum to 100%
- Save results to data/02_revenue_by_tier_q4.json

Should I proceed with writing the main analysis query?
```

**User responds:** "Yes"

---

## Example 3: Time-Series Analysis - Monthly Churn Rate

### Scenario
Calculate monthly churn rate for the past 12 months.

### Phase 0: Load Schema Context

```python
# Use GitHub MCP tool for schema
# Schema provides churn calculation formula:
# churn_rate = (customers_lost / customers_at_start) * 100
```

### Phase 1: Sanity Checks

```python
framework.run_sanity_checks("subscriptions")
```

**Output:**

```
═══════════════════════════════════════════════════════
📋 SANITY CHECK REPORT: subscriptions
═══════════════════════════════════════════════════════

✓ CHECK: Date Range Validation
  What: Ensuring sufficient historical data for 12-month analysis
  Result: PASS
  Details:
    - Earliest record: 2022-03-10
    - Latest record: 2024-12-15
    - Span: 33 months (sufficient for 12-month analysis)

✓ CHECK: Cancellation Date Validity
  What: Checking cancelled_at dates for logic errors
  Result: PASS
  Details:
    - Cancelled subscriptions: 1,234 (39.1%)
    - All cancellation dates >= start_date ✓
    - No future cancellation dates ✓
    - Active subscriptions: 1,922 (60.9%)

✓ CHECK: Date Continuity
  What: Verifying no gaps in monthly data
  Result: PASS
  Details:
    - All 12 months represented (Dec 2023 - Nov 2024)
    - No missing months

═══════════════════════════════════════════════════════
```

### Phase 2: EDA

```python
framework.run_eda("subscriptions", sample_size=1000)
```

**Output:**

```
═══════════════════════════════════════════════════════
📊 EDA REPORT: subscriptions
═══════════════════════════════════════════════════════

DATE COLUMNS:
  • start_date
    Range: 2022-03-10 to 2024-12-15
    Pattern: ~95 new subscriptions/month (last 12 months)

  • cancelled_at
    Records with values: 1,234 (39.1%)
    Records with NULL: 1,922 (60.9% - active subscriptions)
    Pattern: ~40 cancellations/month average

TIME-SERIES PATTERNS:
  • Monthly churn rates (preliminary EDA):
    Dec 2023: 3.2%
    Jan 2024: 3.8%
    Feb 2024: 3.5%
    Mar 2024: 4.1%
    Apr 2024: 3.7%
    May 2024: 3.3%
    Jun 2024: 6.8% ⚠️ (spike - investigate)
    Jul 2024: 4.0%
    Aug 2024: 3.6%
    Sep 2024: 3.4%
    Oct 2024: 3.9%
    Nov 2024: 3.5%

  • Volatility check:
    Average churn: 3.9%
    Standard deviation: 0.9%
    June 2024: +74% above average ⚠️ (investigate cause)

═══════════════════════════════════════════════════════
```

### Phase 3: Present Checkpoint 1

```
---
CHECKPOINT 1: Validation & EDA Complete - Ready for Analysis
---
What I just did:
- Loaded schema.yml from GitHub (churn rate formula confirmed)
- Completed sanity checks on subscriptions: all passed
- Completed EDA: analyzed 3,156 subscriptions over 33 months
- Identified date continuity and preliminary churn patterns

Key findings from validation:
- 3,156 total subscriptions (1,234 cancelled, 1,922 active)
- All 12 months represented with no data gaps
- No invalid dates (all cancellations after start dates)
- Average churn rate: ~3.9% monthly (last 12 months)
- ⚠️ June 2024 churn spike: 6.8% (+74% above average) - requires investigation

Data quality: READY ✅ (with 1 anomaly to investigate)

Next steps:
- Write query to calculate monthly churn rate using schema formula
- Include month-over-month trend analysis
- Investigate June 2024 spike (possible: price increase, product issue, competitor)
- Calculate rolling 3-month average churn
- Save results to data/03_monthly_churn_rate.json

Should I proceed with writing the main analysis query?
```

**User responds:** "Yes, but add a note about the June spike in the analysis"

---

## Example 4: Segment Analysis - User Engagement by Signup Source

### Scenario
Compare user engagement (login frequency) across different signup sources.

### Phase 0: Load Schema Context

```python
# Schema provides:
# - users: user_id, signup_source, created_at
# - login_events: event_id, user_id, login_date
# - Engagement definition: avg logins per user per month
```

### Phase 1: Sanity Checks (Multiple Tables)

```python
framework.run_sanity_checks("users")
framework.run_sanity_checks("login_events")
```

**Output:**

```
═══════════════════════════════════════════════════════
📋 SANITY CHECKS: users + login_events
═══════════════════════════════════════════════════════

✓ CHECK: Segment Completeness (users.signup_source)
  What: Verifying all users are classified
  Result: ⚠️ WARNING
  Details:
    - Google: 4,123 (27.1%)
    - Facebook: 1,441 (9.5%)
    - Email: 7,842 (51.5%)
    - NULL: 1,828 (12.0%)
    - Total: 15,234
    Action: Include NULL as "Unknown" segment

✓ CHECK: Foreign Key Integrity (login_events → users)
  What: Verifying all login events link to valid users
  Result: PASS
  Details:
    - Total login events: 45,678
    - Matched to users: 45,678 (100%)
    - Orphaned: 0 (perfect integrity)

✓ CHECK: Segment Size Adequacy
  What: Ensuring segments are large enough for comparison
  Result: PASS
  Details:
    - Smallest segment (Facebook): 1,441 users
    - All segments >100 (sufficient for analysis)

═══════════════════════════════════════════════════════
```

### Phase 2: EDA

```python
framework.run_eda("login_events", sample_size=2000)
```

**Output:**

```
═══════════════════════════════════════════════════════
📊 EDA REPORT: login_events (by signup_source)
═══════════════════════════════════════════════════════

EVENT DISTRIBUTION BY SOURCE:
  • Google users (4,123 users):
    Total logins: 18,234
    Avg logins/user: 4.42
    Median logins/user: 3
    
  • Facebook users (1,441 users):
    Total logins: 4,987
    Avg logins/user: 3.46
    Median logins/user: 2

  • Email users (7,842 users):
    Total logins: 20,129
    Avg logins/user: 2.57
    Median logins/user: 2

  • Unknown users (1,828 users):
    Total logins: 2,328
    Avg logins/user: 1.27
    Median logins/user: 1

ENGAGEMENT PATTERNS:
  • Google users are most engaged (4.42 logins/user)
  • Facebook users are moderately engaged (3.46 logins/user)
  • Email users are less engaged (2.57 logins/user)
  • Unknown/legacy users have lowest engagement (1.27 logins/user)

KEY INSIGHT:
Social auth users (Google, Facebook) show 35-72% higher engagement
than email signup users. This supports prioritizing social login options.

═══════════════════════════════════════════════════════
```

### Phase 3: Present Checkpoint 1

```
---
CHECKPOINT 1: Validation & EDA Complete - Ready for Analysis
---
What I just did:
- Loaded schema.yml from GitHub (engagement metric definition)
- Completed sanity checks on users + login_events: all passed, 1 warning
- Completed EDA on 45,678 login events across 15,234 users
- Analyzed engagement patterns by signup source

Key findings from validation:
- 4 signup source segments (Google, Facebook, Email, Unknown)
- All segments have sufficient size for statistical comparison (>1,400 users each)
- 100% of login events link to valid users (perfect data integrity)
- Preliminary finding: Social auth users are 35-72% more engaged than email users

Data quality: READY ✅

Next steps:
- Write query to calculate avg logins per user by signup source
- Include confidence intervals for each segment
- Calculate statistical significance of differences
- Visualize engagement comparison
- Save results to data/04_engagement_by_source.json

Should I proceed with writing the main analysis query?
```

---

## Common Patterns Summary

### Pattern 1: Single Table, Simple Metric
- Load schema → Sanity checks → EDA → Checkpoint → Query
- Example: Monthly signups, user counts, revenue totals

### Pattern 2: Multi-Table Join
- Load schema → Sanity checks (all tables) → EDA (all tables) → Join validation → Checkpoint → Query
- Example: Revenue by customer tier, orders by region

### Pattern 3: Time-Series Trend
- Load schema → Sanity checks (date validation) → EDA (temporal patterns) → Volatility checks → Checkpoint → Query
- Example: Monthly churn, weekly active users, daily revenue

### Pattern 4: Segment Comparison
- Load schema → Sanity checks (segment coverage) → EDA (segment distributions) → Size adequacy → Checkpoint → Query
- Example: Engagement by source, revenue by tier, conversion by channel

## Next Steps After Checkpoint 1

Once user approves at Checkpoint 1, proceed to:

1. **Write SQL query** using insights from EDA
2. **Execute query** with validation enabled
3. **Save results** to `data/` folder as JSON
4. **Present Checkpoint 2** with query results
5. Continue to synthesis and report generation




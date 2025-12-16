# Exploratory Data Analysis Report

**Analysis:** MRR by Plan - Last 12 Months  
**Date:** 2024-12-15  
**Analyst:** AI Analytics Hub

---

## 1. Executive Summary

> Key findings from the MRR analysis by plan over the last 12 months.

- **Total MRR Growth**: Overall MRR increased from $7,202 in January 2025 to $9,322 in December 2025, representing a **29.5% growth** over 12 months
- **Plan Performance Divergence**: Free plan shows the highest MRR ($3,158), followed closely by Pro ($3,123) and Enterprise ($3,041) in the most recent month
- **Stability Period**: All three plans have been stable since June 2025, with no month-over-month changes
- **Growth Phase**: Significant growth occurred in Q1 2025, with Enterprise plan showing the highest volatility

---

## 2. Data Overview

### 2.1 Dataset Description

| Metric | Value |
|-----|----|
| Total Records | 36 (12 months × 3 plans) |
| Date Range | January 2025 to December 2025 |
| Unique Plans | 3 (free, pro, enterprise) |
| Data Source | Supabase (public.subscriptions, public.accounts) |

### 2.2 Schema Summary

| Column | Type | Description | % Missing | Unique Values |
|-----|---|----|-----|---|
| month | timestamp | Month of analysis | 0% | 12 |
| plan | text | Subscription plan name | 0% | 3 |
| mrr | numeric | Monthly recurring revenue | 0% | 24 |
| subscription_count | integer | Active subscriptions | 0% | 20 |
| org_count | integer | Unique organizations | 0% | 15 |
| mrr_change_percent | numeric | MoM % change | 8.3% (first month) | 15 |

---

## 3. Data Quality Assessment

### 3.1 Missing Values

**Result: PASS** - No missing values in critical fields.

| Column | Missing Count | Missing % | Handling Strategy |
|-----|---|-----|----|
| month | 0 | 0% | N/A |
| plan | 0 | 0% | N/A |
| mrr | 0 | 0% | N/A |
| mrr_change_percent | 3 | 8.3% | Expected (first month has no previous) |

### 3.2 Duplicates

- **Duplicate rows found:** 0
- **Duplicate key combinations:** None (month + plan is unique)
- **Resolution:** No action needed

### 3.3 Outliers

**Result: ⚠️ WARNING** - Some significant month-over-month changes detected.

| Column | Method | Outliers Found | Range |
|-----|-----|----|----|
| mrr_change_percent | IQR | 3 months with >20% change | -8.99% to +26.45% |

**Notable Outliers:**
- March 2025: Enterprise plan +26.45% growth
- February 2025: Enterprise plan +22.65% growth, Pro plan +20.80% growth
- April 2025: Free plan -8.99% decline, Enterprise plan -5.85% decline

### 3.4 Data Consistency Issues

- **No orphan subscriptions**: All subscriptions have valid org_id references
- **No invalid prices**: All active subscriptions have monthly_price > 0
- **Date continuity**: Complete 12-month series with no gaps
- **Aggregation consistency**: Total MRR sums correctly across plans for each month

---

## 4. Univariate Analysis

### 4.1 Numerical Variables

#### MRR (Monthly Recurring Revenue)
- **Distribution:** Right-skewed with concentration in $2,800-$3,200 range
- **Central Tendency:** Mean = $8,850, Median = $9,322
- **Spread:** Range = $2,201 (min: $7,202, max: $9,401)
- **Notable Observations:** 
  - Lowest MRR: January 2025 ($7,202)
  - Highest MRR: May 2025 ($9,401)
  - Recent stability: June-December 2025 all at $9,322

#### Month-over-Month Change Percentage
- **Distribution:** Bimodal with peaks around 0% (stable) and ±20% (volatile periods)
- **Central Tendency:** Mean = 3.2%, Median = 0.00%
- **Spread:** Std = 10.8%, Range = -8.99% to +26.45%
- **Notable Observations:**
  - 6 months with 0% change (June-December 2025)
  - 3 months with >20% change (February-March 2025)
  - Most volatile: Enterprise plan

### 4.2 Categorical Variables

#### Plan
- **Cardinality:** 3 unique values
- **Top Categories:** 
  1. free: 33.3% of records
  2. pro: 33.3% of records
  3. enterprise: 33.3% of records
- **Notable Observations:** 
  - Equal distribution across plans
  - All plans present in every month
  - No "Unknown" plans found

---

## 5. Bivariate/Multivariate Analysis

### 5.1 Key Relationships

#### MRR by Plan Over Time

**Free Plan:**
- Started at $2,822 in January 2025
- Peaked at $3,183 in March 2025
- Stabilized at $3,158 from May 2025 onwards
- **Total Growth:** +11.9% over 12 months

**Pro Plan:**
- Started at $2,053 in January 2025
- Steady growth through Q1 2025
- Stabilized at $3,123 from May 2025 onwards
- **Total Growth:** +52.1% over 12 months (highest growth)

**Enterprise Plan:**
- Started at $2,327 in January 2025
- Highest volatility with peaks and valleys
- Peaked at $3,609 in March 2025
- Stabilized at $3,041 from June 2025 onwards
- **Total Growth:** +30.7% over 12 months

### 5.2 Segmentation Findings

**Growth Segments:**
1. **High Growth (Jan-Mar 2025)**: All plans showing strong growth
2. **Consolidation (Apr-May 2025)**: Some plans declining, others growing
3. **Stability (Jun-Dec 2025)**: All plans flat with no changes

**Plan Performance Segments:**
1. **Pro Plan**: Highest growth rate (+52.1%) but started from lowest base
2. **Enterprise Plan**: Most volatile, highest peak ($3,609)
3. **Free Plan**: Most stable, consistent growth pattern

---

## 6. Time-Based Patterns

- **Trend:** Overall increasing from $7,202 to $9,322 (+29.5%)
- **Seasonality:** No clear seasonal pattern detected in 12-month window
- **Anomalies:** 
  - March 2025: Enterprise plan spike (+26.45%)
  - April 2025: Free plan decline (-8.99%)
  - June-December 2025: Complete stability (0% change across all plans)

---

## 7. Data Quality Score

| Dimension | Score (1-5) | Notes |
|-----|----|----|
| Completeness | 5 | No missing values in critical fields |
| Accuracy | 5 | All joins valid, aggregations consistent |
| Consistency | 5 | Data structure consistent across months |
| Timeliness | 5 | Data covers full 12-month period |
| **Overall** | **5** | Excellent data quality |

---

## 8. Recommendations for Analysis

1. **Include:** All three plans in analysis (all have meaningful data)
2. **Exclude:** None - all data points are valid
3. **Transform:** Consider smoothing for Enterprise plan volatility analysis
4. **Investigate Further:** 
   - Why did all plans stabilize in June 2025?
   - What caused Enterprise plan volatility in Q1 2025?
   - Is the current stability sustainable?

---

## Appendix

### A. Queries Used
- [Query 1: MRR by Plan - Last 12 Months](../queries/01_mrr-by-plan-last-12-months.sql)

### B. Validation Checks
- ✓ Join Validation: No orphan subscriptions
- ✓ Aggregation Sanity: All totals consistent
- ✓ Time-Series Validation: Complete date coverage
- ✓ Segment Validation: All plans present in all months

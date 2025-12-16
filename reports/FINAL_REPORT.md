# B2B SaaS User Activity Analysis - Final Report

**Generated:** 2025-12-15 11:05:56

---

## Executive Summary

This report presents a comprehensive analysis of B2B SaaS user activity data, including data quality validation, exploratory data analysis, and engagement weight calculations for a churn prediction scoring model.

**Dataset Overview:**
- **Total Records:** 50,000
- **Total Columns:** 9
- **Memory Usage:** 8.06 MB

---

## 1. Data Quality Sanity Check

### 1.1 Missing Values

✅ **PASS:** No missing values found in any column.

All columns are complete with no null values detected.

### 1.2 Duplicate Records

✅ **PASS:** No duplicate rows found.

✅ **PASS:** No duplicate User_IDs found.


### 1.3 Data Types

| Column | Data Type | Non-Null Count | Total Count |
|--------|-----------|----------------|-------------|
| `User_ID` | object | 50,000 | 50,000 |
| `Subscription_Tier` | object | 50,000 | 50,000 |
| `Num_Logins` | int64 | 50,000 | 50,000 |
| `Num_Searches` | int64 | 50,000 | 50,000 |
| `Num_Card_Views` | int64 | 50,000 | 50,000 |
| `Num_API_Calls` | int64 | 50,000 | 50,000 |
| `Num_Exports` | int64 | 50,000 | 50,000 |
| `Num_Emails_Sent` | int64 | 50,000 | 50,000 |
| `Churned` | int64 | 50,000 | 50,000 |

---

## 2. Target Variable Analysis

### 2.1 Churn Distribution

| Status | Count | Percentage |
|--------|-------|------------|
| **Retained (0)** | 44,943 | 89.89% |
| **Churned (1)** | 5,057 | 10.11% |

**Key Findings:**
- **Retention Rate:** 89.89%
- **Churn Rate:** 10.11%
- The dataset shows a healthy retention rate with approximately 9 out of 10 users being retained.

**Visualization:** See `churn_distribution.png`

---

## 3. Activity Metrics vs Churn Analysis

### 3.1 Activity Comparison

Boxplots comparing activity metrics between Retained and Churned users reveal behavioral differences:

**Visualization:** See `activity_vs_churn_boxplots.png`

**Key Metrics Analyzed:**
- `Num_Exports`
- `Num_Logins`
- `Num_API_Calls`

---

## 4. Correlation Analysis

### 4.1 Correlation with Churn Status

All activity metrics show **negative correlations** with churn, which is expected: higher activity levels are associated with lower churn rates.

| Activity Metric | Correlation with Churn | Interpretation |
|-----------------|------------------------|----------------|
| `Num_Logins` | -0.1024 | Strong negative correlation - Higher num_logins associated with lower churn |
| `Num_Searches` | -0.0837 | Moderate negative correlation - Higher num_searches associated with lower churn |
| `Num_Card_Views` | -0.0915 | Moderate negative correlation - Higher num_card_views associated with lower churn |
| `Num_API_Calls` | -0.0972 | Moderate negative correlation - Higher num_api_calls associated with lower churn |
| `Num_Exports` | -0.1237 | Strong negative correlation - Higher num_exports associated with lower churn |
| `Num_Emails_Sent` | -0.1256 | Strong negative correlation - Higher num_emails_sent associated with lower churn |

**Visualization:** See `correlation_heatmap.png`

### 4.2 Correlation Insights

- **Strongest Predictors of Retention:**
  1. `Num_Emails_Sent` (correlation: -0.1256)
  2. `Num_Exports` (correlation: -0.1237)

- **Moderate Predictors:**
  3. `Num_Logins` (correlation: -0.1024)
  4. `Num_API_Calls` (correlation: -0.0972)
  5. `Num_Card_Views` (correlation: -0.0915)

- **Weakest Predictor:**
  6. `Num_Searches` (correlation: -0.0837)

---

## 5. Engagement Weights Calculation

### 5.1 Methodology

1. **Invert Correlations:** Multiply by -1 (negative correlation with Churn = positive impact on Retention)
2. **Normalize to 1-10 Scale:** Transform inverted correlations to weights where 10 = most impactful feature

**Normalization Formula:**
```
weight = 1 + (inverted_correlation - min) / (max - min) × 9
```

**Normalization Parameters:**
- Minimum inverted correlation: 0.0837
- Maximum inverted correlation: 0.1256
- Range: 0.0419

### 5.2 Inverted Correlations

| Activity Metric | Original Correlation | Inverted Correlation |
|-----------------|---------------------|---------------------|
| `Num_Logins` | -0.1024 | 0.1024 |
| `Num_Searches` | -0.0837 | 0.0837 |
| `Num_Card_Views` | -0.0915 | 0.0915 |
| `Num_API_Calls` | -0.0972 | 0.0972 |
| `Num_Exports` | -0.1237 | 0.1237 |
| `Num_Emails_Sent` | -0.1256 | 0.1256 |

### 5.3 Final Engagement Weights

**AI-Recommended Weights for Scoring Model (1-10 Scale):**

| Activity Metric | Weight | Impact Level |
|-----------------|--------|--------------|
| `Num_Emails_Sent` | **10.00** | 🔴 Very High |
| `Num_Exports` | **9.58** | 🔴 Very High |
| `Num_Logins` | **5.03** | 🟡 Medium |
| `Num_API_Calls` | **3.91** | 🟢 Low |
| `Num_Card_Views` | **2.69** | ⚪ Very Low |
| `Num_Searches` | **1.00** | ⚪ Very Low |

**Visualization:** See `engagement_weights_bar_chart.png`

### 5.4 Python Dictionary (Ready to Use)

```python
weights = {
    'Num_Emails_Sent': 10.00,
    'Num_Exports': 9.58,
    'Num_Logins': 5.03,
    'Num_API_Calls': 3.91,
    'Num_Card_Views': 2.69,
    'Num_Searches': 1.00,
}
```

---

## 6. Key Insights & Recommendations

### 6.1 Data Quality

✅ **Excellent Data Quality:** The dataset is clean with no missing values, duplicates, or data quality issues detected. Safe to proceed with analysis.

### 6.2 Engagement Insights

1. **Top Engagement Indicators:**
   - `Num_Emails_Sent` (Weight: 10.00) - Users who send emails are highly engaged
   - `Num_Exports` (Weight: 9.58) - Export activity indicates strong product value

2. **Moderate Engagement Indicators:**
   - `Num_Logins` (Weight: 5.03) - Regular logins show consistent usage
   - `Num_API_Calls` (Weight: 3.91) - API usage indicates integration/automation

3. **Lower Engagement Indicators:**
   - `Num_Card_Views` (Weight: 2.69) - Passive viewing behavior
   - `Num_Searches` (Weight: 1.00) - Search activity alone is less predictive

### 6.3 Model Recommendations

1. **Scoring Model:** Use the calculated weights to create an engagement score:
   ```
   Engagement Score = Σ(Activity_Metric × Weight)
   ```

2. **Feature Priority:** Focus retention efforts on users with low `Num_Emails_Sent` and `Num_Exports` as these are the strongest predictors.

3. **Threshold Setting:** Consider setting engagement score thresholds based on the churn rate distribution to identify at-risk users.

---

## 7. Generated Visualizations

1. **`churn_distribution.png`** - Distribution of Retained vs Churned users
2. **`activity_vs_churn_boxplots.png`** - Boxplots comparing activity metrics
3. **`correlation_heatmap.png`** - Correlation matrix heatmap
4. **`engagement_weights_bar_chart.png`** - Visual representation of calculated weights

---

## 8. Data Sample

### First 10 Rows

```
      User_ID Subscription_Tier  Num_Logins  Num_Searches  Num_Card_Views  Num_API_Calls  Num_Exports  Num_Emails_Sent  Churned
0  USER_00000               Pro           8            27              53            108            3                2        0
1  USER_00001        Enterprise          19            69             148           2493           12               27        0
2  USER_00002        Enterprise          13            71             146           2401           12               29        0
3  USER_00003               Pro          11            13              53             85            0                1        1
4  USER_00004               Pro           8            30               0             86            5               10        0
5  USER_00005               Pro           8            18              58             98            2                5        0
6  USER_00006               Pro          10            33              59            104            0                7        0
7  USER_00007        Enterprise          24            50             147           2494            6               32        0
8  USER_00008               Pro           8            23              52             93            2                2        0
9  USER_00009        Enterprise          21            70             158           2415            9               22        0
```

---

## Appendix: Statistical Summary

### Activity Metrics Summary Statistics


**Num_Logins:**
- Mean: 10.96
- Median: 9.00
- Std Dev: 6.73
- Min: 0
- Max: 40

**Num_Searches:**
- Mean: 33.65
- Median: 27.00
- Std Dev: 18.32
- Min: 0
- Max: 92

**Num_Card_Views:**
- Mean: 75.85
- Median: 53.00
- Std Dev: 48.59
- Min: 0
- Max: 201

**Num_API_Calls:**
- Mean: 772.75
- Median: 104.00
- Std Dev: 1084.37
- Min: 0
- Max: 2681

**Num_Exports:**
- Mean: 4.16
- Median: 2.00
- Std Dev: 4.21
- Min: 0
- Max: 26

**Num_Emails_Sent:**
- Mean: 11.81
- Median: 6.00
- Std Dev: 11.95
- Min: 0
- Max: 54


---

**Report Generated:** 2025-12-15 11:05:56
**Analysis Framework:** Python 3 with pandas, numpy, matplotlib, seaborn

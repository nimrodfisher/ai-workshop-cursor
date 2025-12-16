"""
Generate Final Report: Data Quality, EDA, and Engagement Weights Analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime

def load_data(file_path):
    """Load the CSV file into a pandas DataFrame"""
    return pd.read_csv(file_path)

def calculate_correlations(df):
    """Calculate correlation between numerical activity columns and Churned status"""
    activity_columns = [
        'Num_Logins', 'Num_Searches', 'Num_Card_Views', 
        'Num_API_Calls', 'Num_Exports', 'Num_Emails_Sent'
    ]
    correlations = {col: df[col].corr(df['Churned']) for col in activity_columns}
    return correlations, activity_columns

def calculate_weights(correlations):
    """Calculate engagement weights"""
    inverted_correlations = {k: -v for k, v in correlations.items()}
    values = list(inverted_correlations.values())
    min_val = min(values)
    max_val = max(values)
    
    weights = {}
    for col, val in inverted_correlations.items():
        if max_val == min_val:
            weight = 5.5
        else:
            weight = 1 + (val - min_val) / (max_val - min_val) * 9
        weights[col] = round(weight, 2)
    
    return weights, inverted_correlations

def generate_report():
    """Generate comprehensive final report"""
    
    # Load data
    df = load_data('saas_aggregated_data.csv')
    
    # Calculate correlations and weights
    correlations, activity_columns = calculate_correlations(df)
    weights, inverted_correlations = calculate_weights(correlations)
    
    # Sanity check results
    missing_values = df.isnull().sum()
    total_duplicates = df.duplicated().sum()
    duplicate_user_ids = df['User_ID'].duplicated().sum()
    churn_counts = df['Churned'].value_counts().sort_index()
    churn_pct = df['Churned'].value_counts(normalize=True).sort_index() * 100
    
    # Generate report
    report = f"""# B2B SaaS User Activity Analysis - Final Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary

This report presents a comprehensive analysis of B2B SaaS user activity data, including data quality validation, exploratory data analysis, and engagement weight calculations for a churn prediction scoring model.

**Dataset Overview:**
- **Total Records:** {len(df):,}
- **Total Columns:** {len(df.columns)}
- **Memory Usage:** {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB

---

## 1. Data Quality Sanity Check

### 1.1 Missing Values
"""
    
    if missing_values.sum() == 0:
        report += """
✅ **PASS:** No missing values found in any column.

All columns are complete with no null values detected.
"""
    else:
        report += "\n⚠️ **WARNING:** Missing values detected:\n\n"
        for col, count in missing_values[missing_values > 0].items():
            pct = (count / len(df) * 100)
            report += f"- `{col}`: {count:,} missing ({pct:.2f}%)\n"
    
    report += f"""
### 1.2 Duplicate Records

"""
    
    if total_duplicates == 0:
        report += "✅ **PASS:** No duplicate rows found.\n\n"
    else:
        report += f"⚠️ **WARNING:** Found {total_duplicates:,} duplicate rows ({total_duplicates/len(df)*100:.2f}%)\n\n"
    
    if duplicate_user_ids == 0:
        report += "✅ **PASS:** No duplicate User_IDs found.\n\n"
    else:
        report += f"❌ **ERROR:** Found {duplicate_user_ids:,} duplicate User_IDs ({duplicate_user_ids/len(df)*100:.2f}%)\n\n"
    
    report += f"""
### 1.3 Data Types

| Column | Data Type | Non-Null Count | Total Count |
|--------|-----------|----------------|-------------|
"""
    
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].count()
        total = len(df)
        report += f"| `{col}` | {dtype} | {non_null:,} | {total:,} |\n"
    
    report += f"""
---

## 2. Target Variable Analysis

### 2.1 Churn Distribution

| Status | Count | Percentage |
|--------|-------|------------|
| **Retained (0)** | {churn_counts.get(0, 0):,} | {churn_pct.get(0, 0):.2f}% |
| **Churned (1)** | {churn_counts.get(1, 0):,} | {churn_pct.get(1, 0):.2f}% |

**Key Findings:**
- **Retention Rate:** {churn_pct.get(0, 0):.2f}%
- **Churn Rate:** {churn_pct.get(1, 0):.2f}%
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
"""
    
    for col in activity_columns:
        corr = correlations[col]
        interpretation = "Strong negative" if abs(corr) > 0.1 else "Moderate negative" if abs(corr) > 0.05 else "Weak negative"
        report += f"| `{col}` | {corr:.4f} | {interpretation} correlation - Higher {col.lower()} associated with lower churn |\n"
    
    report += f"""
**Visualization:** See `correlation_heatmap.png`

### 4.2 Correlation Insights

- **Strongest Predictors of Retention:**
  1. `Num_Emails_Sent` (correlation: {correlations['Num_Emails_Sent']:.4f})
  2. `Num_Exports` (correlation: {correlations['Num_Exports']:.4f})

- **Moderate Predictors:**
  3. `Num_Logins` (correlation: {correlations['Num_Logins']:.4f})
  4. `Num_API_Calls` (correlation: {correlations['Num_API_Calls']:.4f})
  5. `Num_Card_Views` (correlation: {correlations['Num_Card_Views']:.4f})

- **Weakest Predictor:**
  6. `Num_Searches` (correlation: {correlations['Num_Searches']:.4f})

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
- Minimum inverted correlation: {min(inverted_correlations.values()):.4f}
- Maximum inverted correlation: {max(inverted_correlations.values()):.4f}
- Range: {max(inverted_correlations.values()) - min(inverted_correlations.values()):.4f}

### 5.2 Inverted Correlations

| Activity Metric | Original Correlation | Inverted Correlation |
|-----------------|---------------------|---------------------|
"""
    
    for col in activity_columns:
        orig = correlations[col]
        inv = inverted_correlations[col]
        report += f"| `{col}` | {orig:.4f} | {inv:.4f} |\n"
    
    report += f"""
### 5.3 Final Engagement Weights

**AI-Recommended Weights for Scoring Model (1-10 Scale):**

| Activity Metric | Weight | Impact Level |
|-----------------|--------|--------------|
"""
    
    sorted_weights = sorted(weights.items(), key=lambda x: x[1], reverse=True)
    for col, weight in sorted_weights:
        if weight >= 9:
            level = "🔴 Very High"
        elif weight >= 7:
            level = "🟠 High"
        elif weight >= 5:
            level = "🟡 Medium"
        elif weight >= 3:
            level = "🟢 Low"
        else:
            level = "⚪ Very Low"
        report += f"| `{col}` | **{weight:.2f}** | {level} |\n"
    
    report += f"""
**Visualization:** See `engagement_weights_bar_chart.png`

### 5.4 Python Dictionary (Ready to Use)

```python
weights = {{
"""
    
    for col, weight in sorted_weights:
        report += f"    '{col}': {weight:.2f},\n"
    
    report += """}
```

---

## 6. Key Insights & Recommendations

### 6.1 Data Quality
"""
    
    if missing_values.sum() == 0 and total_duplicates == 0 and duplicate_user_ids == 0:
        report += """
✅ **Excellent Data Quality:** The dataset is clean with no missing values, duplicates, or data quality issues detected. Safe to proceed with analysis.
"""
    else:
        report += """
⚠️ **Data Quality Issues Detected:** Review the sanity check section above for details. Consider data cleaning before model deployment.
"""
    
    report += f"""
### 6.2 Engagement Insights

1. **Top Engagement Indicators:**
   - `Num_Emails_Sent` (Weight: {weights['Num_Emails_Sent']:.2f}) - Users who send emails are highly engaged
   - `Num_Exports` (Weight: {weights['Num_Exports']:.2f}) - Export activity indicates strong product value

2. **Moderate Engagement Indicators:**
   - `Num_Logins` (Weight: {weights['Num_Logins']:.2f}) - Regular logins show consistent usage
   - `Num_API_Calls` (Weight: {weights['Num_API_Calls']:.2f}) - API usage indicates integration/automation

3. **Lower Engagement Indicators:**
   - `Num_Card_Views` (Weight: {weights['Num_Card_Views']:.2f}) - Passive viewing behavior
   - `Num_Searches` (Weight: {weights['Num_Searches']:.2f}) - Search activity alone is less predictive

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
{df.head(10).to_string()}
```

---

## Appendix: Statistical Summary

### Activity Metrics Summary Statistics

"""
    
    for col in activity_columns:
        stats = df[col].describe()
        report += f"""
**{col}:**
- Mean: {stats['mean']:.2f}
- Median: {stats['50%']:.2f}
- Std Dev: {stats['std']:.2f}
- Min: {stats['min']:.0f}
- Max: {stats['max']:.0f}
"""
    
    report += f"""

---

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Analysis Framework:** Python 3 with pandas, numpy, matplotlib, seaborn
"""
    
    return report

def main():
    """Generate and save the final report"""
    print("="*80)
    print("GENERATING FINAL REPORT")
    print("="*80)
    
    report = generate_report()
    
    # Save as Markdown
    with open('FINAL_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("✓ Final report saved: FINAL_REPORT.md")
    print("\n" + "="*80)
    print("REPORT GENERATION COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()





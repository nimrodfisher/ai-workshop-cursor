# New Analysis Framework Features

## Overview

The analysis framework has been enhanced with four major new capabilities:

1. **Sanity Checks** - Data quality validation
2. **EDA (Exploratory Data Analysis)** - Comprehensive data exploration
3. **Text Classification** - LLM-based text categorization
4. **Diagnostic Analysis** - Segment comparison and insights

## 1. Sanity Checks

### Purpose
Automatically validate data quality before analysis to catch issues early.

### Features
- **Null Checks**: Identifies missing values in critical columns
- **Duplicate Detection**: Finds duplicate records and business keys
- **Consistency Validation**: Checks date ranges, numeric ranges, enum values
- **Completeness Checks**: Validates required fields are populated

### Configuration
Rules are defined in `sanity_check_rules.yml`:
- Table-specific rules
- Severity levels (error, warning, info)
- Custom thresholds

### Usage
```python
# Run sanity checks on a table
sanity_results = framework.run_sanity_checks("users")
```

### Output
- Summary of checks (passed/warnings/errors)
- Detailed results for each check type
- Severity-based reporting

## 2. EDA (Exploratory Data Analysis)

### Purpose
Comprehensive exploration of data to understand distributions, relationships, and patterns.

### Features
- **Basic Statistics**: Row counts, column info, null summaries
- **Distribution Analysis**: Skewness, outliers, zero inflation
- **Relationship Analysis**: Correlations between numeric columns
- **Time-Series Analysis**: Temporal patterns and gaps
- **Automatic Flags**: Identifies potential issues
- **Typical Questions**: Raises common questions about the data

### Configuration
Rules are defined in `eda_rules.yml`:
- EDA phases configuration
- Flag conditions
- Typical questions to raise

### Usage
```python
# Run EDA on a table
eda_results = framework.run_eda("users", sample_size=1000)
```

### Output
- Basic statistics summary
- Distribution information
- Correlation matrices
- Flags and typical questions

## 3. Text Classification

### Purpose
Use LLM to classify text data into meaningful categories based on user context.

### Features
- **Context-Driven**: Uses user's context to create relevant categories
- **LLM-Based**: Leverages language models for intelligent classification
- **Flexible Categories**: Creates custom buckets based on analysis needs
- **Analysis Ready**: Provides classified data ready for analysis

### Usage
```python
# Classify text column
classification = framework.classify_text_column(
    table_name="support_tickets",
    column_name="category",
    user_context="Classify by urgency and type",
    num_categories=5
)
```

### Workflow
1. User provides context for classification
2. Framework samples unique values
3. LLM creates categories based on context
4. Values are mapped to categories
5. Classified data is analyzed

## 4. Diagnostic Analysis & Segment Comparison

### Purpose
Compare segments to identify performance gaps and generate insights.

### Features
- **Segment Comparison**: Compare any segments on target metrics
- **Statistical Testing**: T-tests for significance
- **Performance Gaps**: Identifies best/worst performing segments
- **Insight Generation**: Automatic insight creation

### Usage
```python
# Compare segments
diagnostic = framework.run_diagnostic_analysis(
    query="SELECT plan, monthly_price FROM subscriptions...",
    target_column="monthly_price",
    segment_columns=["plan", "industry"],
    description="Compare subscription prices across plans"
)
```

### Output
- Segment statistics (mean, median, std, etc.)
- Pairwise comparisons
- Statistical significance tests
- Performance gap insights

## Complete Workflow

### Recommended Analysis Flow

1. **Sanity Checks** (Phase 1)
   - Validate data quality
   - Catch issues early
   - Understand data completeness

2. **EDA** (Phase 2)
   - Explore data distributions
   - Identify patterns
   - Raise flags and questions

3. **Main Analysis** (Phase 3)
   - Run your analysis queries
   - Validate aggregations
   - Get results

4. **Text Classification** (Phase 4 - if needed)
   - Classify text columns
   - Create new categories
   - Analyze classified data

5. **Diagnostic Analysis** (Phase 5)
   - Compare segments
   - Identify performance gaps
   - Generate insights

## Example: Complete Analysis

```python
from analysis_framework import AnalysisFramework

framework = AnalysisFramework()
framework.connect()

# Phase 1: Sanity Checks
framework.run_sanity_checks("users")
framework.run_sanity_checks("subscriptions")

# Phase 2: EDA
framework.run_eda("users", sample_size=1000)
framework.run_eda("events", sample_size=5000)

# Phase 3: Main Analysis
step = framework.add_step(
    description="Calculate MRR by plan",
    query="SELECT plan, SUM(monthly_price) as mrr FROM ...",
    validate=True,
    aggregation_column="mrr",
    segment_columns=["plan"],
    table_name="subscriptions"
)

# Phase 4: Text Classification (if needed)
# classification = framework.classify_text_column(...)

# Phase 5: Diagnostic Analysis
diagnostic = framework.run_diagnostic_analysis(
    query="SELECT plan, monthly_price FROM subscriptions...",
    target_column="monthly_price",
    segment_columns=["plan"]
)

framework.close()
```

## Configuration Files

### `sanity_check_rules.yml`
- Define sanity check rules
- Configure table-specific checks
- Set severity levels

### `eda_rules.yml`
- Configure EDA phases
- Define flag conditions
- Set typical questions

## Benefits

1. **Data Quality**: Catch issues before analysis
2. **Understanding**: Comprehensive EDA reveals patterns
3. **Flexibility**: Text classification adapts to your needs
4. **Insights**: Diagnostic analysis finds performance gaps
5. **Transparency**: All steps are documented and explained

## Next Steps

1. Review `sanity_check_rules.yml` and customize for your data
2. Review `eda_rules.yml` and adjust for your analysis needs
3. Run `analysis_workflow_enhanced_example.py` to see all features
4. Integrate into your analysis workflows


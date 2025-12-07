# Usage Guide: Analysis Framework in Cursor

## Overview

This framework runs analysis workflows directly in Cursor chat. When you need a dashboard, it generates an HTML mockup.

## Quick Start

### 1. Basic Analysis

Ask me to run an analysis:

```
"Analyze our MRR by plan"
"Show me user distribution by role"
"What's our revenue trend over time?"
```

I'll:
- Load schema from your GitHub repo
- Run transparent analysis steps
- Validate aggregations
- Show results in chat

### 2. Request a Dashboard

After analysis, ask for a dashboard:

```
"Create a dashboard for this analysis"
"Generate a visualization of these results"
"Make an HTML dashboard"
```

I'll:
- Extract data from analysis results
- Generate interactive HTML dashboard
- Save as `dashboard_YYYYMMDD_HHMMSS.html`
- Tell you where to find it

### 3. Open Dashboard

Simply open the HTML file in any browser - no server needed!

## Example Conversation Flow

**You**: "What's our MRR by plan?"

**Me**: 
```
📚 Loading schema context from GitHub...
✅ Analysis framework initialized

🔍 Analysis Question: What's our MRR by plan?
📊 Tables identified: ['subscriptions', 'accounts']

================================================================================
STEP 1: Understanding the data
================================================================================

📊 What this step does:
   First, let's check if we have subscription data...

📈 Results:
   • Rows returned: 120
   • Execution time: 0.023 seconds

[... more steps ...]

✅ All validation cases passed!
```

**You**: "Create a dashboard for this"

**Me**:
```
✅ Dashboard created: dashboard_20241215_143022.html
📂 Open in browser to view
```

## Analysis Features

### Transparent Steps
Each step shows:
- What it does (plain language)
- Assumptions made
- Clarifications needed
- Query executed
- Results summary
- Performance warnings
- Validation results

### Validation
After aggregations:
- Selects 2-3 sample segments
- Queries raw data
- Recalculates manually
- Compares results
- Reports status

### Performance Awareness
Automatically:
- Checks table sizes
- Warns about large tables
- Suggests filters
- Tracks execution time

## Dashboard Features

### What You Get
- **Metric Cards**: Key numbers with formatting
- **Interactive Charts**: Bar, line, pie charts
- **Data Tables**: Formatted results
- **Responsive Design**: Works on all devices
- **Standalone**: No server needed

### Chart Types
- **Bar Charts**: Comparisons
- **Line Charts**: Trends
- **Pie Charts**: Distributions

## Advanced Usage

### Custom Analysis Steps

You can define custom analysis workflows:

```python
from analysis_runner import AnalysisRunner

runner = AnalysisRunner()
runner.initialize()

steps = [
    {
        'description': "Calculate MRR by plan",
        'query': """
            SELECT plan, SUM(monthly_price) as mrr
            FROM subscriptions s
            JOIN accounts a ON s.org_id = a.id
            WHERE s.status = 'active'
            GROUP BY plan;
        """,
        'assumptions': ["Only active subscriptions count"],
        'clarifications': ["Should we include trials?"],
        'validate': True,
        'aggregation_column': 'mrr',
        'segment_columns': ['plan'],
        'table_name': 'subscriptions'
    }
]

results = runner.run_analysis("What's our MRR by plan?", steps)
```

### Custom Dashboard

```python
dashboard_config = {
    'title': 'Custom Dashboard',
    'include_metrics': [
        {'label': 'Total MRR', 'value': 50000, 'format': 'currency'}
    ],
    'include_charts': [
        {
            'chart_type': 'bar',
            'data': [{'plan': 'Pro', 'mrr': 30000}, ...],
            'title': 'MRR by Plan',
            'x_column': 'plan',
            'y_column': 'mrr'
        }
    ]
}

dashboard_path = runner.create_dashboard(dashboard_config)
```

## Tips

1. **Start Simple**: Ask basic questions first
2. **Build Gradually**: Add complexity step by step
3. **Request Dashboards**: When you need visualizations
4. **Review Validation**: Check validation results
5. **Use Context**: Framework uses your schema automatically

## Troubleshooting

### Schema Not Loading
- Check GitHub repo name
- Ensure `schema.yml` exists in repo
- Verify internet connection

### Validation Failures
- Review raw data queries
- Check for data quality issues
- Verify aggregation logic

### Dashboard Not Generating
- Ensure analysis completed first
- Check data format
- Review dashboard config

## Next Steps

1. Try asking a simple question
2. Request a dashboard
3. Explore the HTML file
4. Customize for your needs



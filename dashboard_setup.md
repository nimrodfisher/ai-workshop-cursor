# Dashboard & Visualization Guide

## Analysis Workflow in Cursor

The analysis framework runs directly in Cursor chat. When you need a dashboard, it generates an HTML mockup that you can open in any browser.

## HTML Dashboard Generation

When you request a dashboard, the framework creates a standalone HTML file with:

- **Interactive Charts**: Using Chart.js (bar, line, pie charts)
- **Metric Cards**: Key metrics with formatting (currency, percentages, numbers)
- **Data Tables**: Formatted tables with hover effects
- **Responsive Design**: Works on desktop and mobile
- **No Dependencies**: Standalone HTML file - just open in browser

## Usage

### Running Analysis in Cursor

```python
from analysis_runner import AnalysisRunner

runner = AnalysisRunner()
runner.initialize()

# Run analysis
steps = [
    {
        'description': "Calculate MRR by plan",
        'query': "SELECT plan, SUM(monthly_price) as mrr FROM ...",
        'validate': True,
        'aggregation_column': 'mrr',
        'segment_columns': ['plan'],
        'table_name': 'subscriptions'
    }
]

results = runner.run_analysis("What's our MRR by plan?", steps)
```

### Creating a Dashboard

When you ask for a dashboard, the framework will:

1. Extract data from analysis results
2. Generate interactive HTML dashboard
3. Save as `dashboard_YYYYMMDD_HHMMSS.html`
4. You can open it in any browser

```python
# After running analysis, create dashboard
dashboard_path = runner.create_dashboard({
    'title': 'MRR Analysis Dashboard',
    'include_metrics': [
        {'label': 'Total MRR', 'value': 50000, 'format': 'currency'}
    ],
    'include_charts': [
        {
            'chart_type': 'bar',
            'data': [...],  # Your data
            'title': 'MRR by Plan',
            'x_column': 'plan',
            'y_column': 'mrr'
        }
    ]
})
```

## Dashboard Features

### Metric Cards
- Large, readable numbers
- Formatting: currency, percentages, numbers
- Optional change indicators

### Charts
- **Bar Charts**: For comparisons
- **Line Charts**: For trends over time
- **Pie Charts**: For distributions

### Tables
- Formatted data tables
- Hover effects
- Responsive scrolling

## Example Workflow

1. **Ask a question in Cursor**: "What's our MRR by plan?"
2. **Framework runs analysis**: Transparent steps with validation
3. **Request dashboard**: "Create a dashboard for this analysis"
4. **Get HTML file**: Open `dashboard_*.html` in browser
5. **Share**: Send HTML file to team members

## Benefits

- ✅ No server needed - just HTML file
- ✅ Works offline
- ✅ Easy to share
- ✅ No dependencies to install
- ✅ Generated on-demand
- ✅ Based on your actual analysis results

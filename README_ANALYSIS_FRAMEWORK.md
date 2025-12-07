# Analysis Framework Documentation

## Overview

This analysis framework implements a comprehensive, transparent, and validated approach to data analysis with four key principles:

1. **Performance** - Query optimization based on metadata context
2. **Validation** - Automatic validation after aggregations using raw data samples
3. **Gradual Process** - Transparent step-by-step analysis with explanations
4. **Context-Aware** - Combines schema from GitHub + user input + real-time data checks

## Key Components

### 1. `analysis_framework.py`
Main framework that orchestrates the analysis process.

**Key Features:**
- Performance-aware querying based on table metadata
- Automatic validation of aggregations
- Step-by-step transparent process
- Execution time tracking
- Query plan analysis

**Usage:**
```python
from analysis_framework import AnalysisFramework

framework = AnalysisFramework()
framework.connect()

# Add analysis step with validation
step = framework.add_step(
    description="Calculate MRR by plan",
    query="SELECT plan, SUM(monthly_price) as mrr FROM ...",
    validate=True,
    aggregation_column="mrr",
    segment_columns=["plan"],
    table_name="subscriptions"
)

framework.print_step_summary(step)
```

### 2. `context_manager.py`
Manages context from multiple sources.

**Sources:**
- **Schema from GitHub**: Loads schema.yml from your repo
- **User Input**: Captures questions and clarifications
- **Real-time Data**: Checks actual data in database

**Usage:**
```python
from context_manager import ContextManager

context = ContextManager("nimrodfisher", "workshop-queries-repo")
context.load_schema_from_github("schema.yml")
context.add_user_context("What's our MRR?")
mapping = context.map_user_question_to_schema("What's our MRR?")
```

### 3. `analysis_workflow_example.py`
Complete example showing the framework in action.

## Analysis Flow

### Step 1: Context Gathering
```
1. Load schema from GitHub repo
2. Capture user question/requirements
3. Map user question to schema elements
4. Check real-time data metadata
```

### Step 2: Gradual Analysis
```
For each analysis step:
1. Explain what the step does (plain language)
2. List assumptions made
3. Ask for clarifications if needed
4. Check performance considerations
5. Execute query
6. Validate results (if aggregation)
7. Display transparent summary
```

### Step 3: Validation Process
```
After each aggregation:
1. Select 2-3 sample segments
2. Query raw data for each segment
3. Manually calculate expected value
4. Compare with aggregated result
5. Report validation status
```

## Performance Considerations

The framework automatically:
- Checks table row counts
- Warns about large tables (>1M rows)
- Suggests date filters for time-series tables
- Provides query execution time
- Analyzes query plans

## Validation Process

When `validate=True` is set on an aggregation step:

1. **Sample Selection**: Picks 2-3 segments from aggregated results
2. **Raw Data Query**: Queries original table for those segments
3. **Manual Calculation**: Recalculates aggregation on raw data
4. **Comparison**: Compares expected vs actual
5. **Reporting**: Shows validation status for each case

Example validation output:
```
✅ Validation results:
   ✓ PASSED: Validation for segment: {'plan': 'Pro'}
      Expected: 5000.00, Actual: 5000.00
      Checked 15 raw records
   ✓ PASSED: Validation for segment: {'plan': 'Enterprise'}
      Expected: 12000.00, Actual: 12000.00
      Checked 8 raw records
```

## Usage Examples

### Basic Analysis
```python
from analysis_framework import AnalysisFramework

framework = AnalysisFramework()
framework.connect()

step = framework.add_step(
    description="Count total users",
    query="SELECT COUNT(*) FROM users;"
)

framework.print_step_summary(step)
framework.close()
```

### Analysis with Validation
```python
step = framework.add_step(
    description="Calculate MRR by plan",
    query="""
        SELECT plan, SUM(monthly_price) as mrr
        FROM subscriptions s
        JOIN accounts a ON s.org_id = a.id
        WHERE s.status = 'active'
        GROUP BY plan;
    """,
    assumptions=["Only active subscriptions count"],
    clarifications=["Should we include trials?"],
    validate=True,
    aggregation_column="mrr",
    segment_columns=["plan"],
    table_name="subscriptions"
)
```

### Context-Aware Analysis
```python
from context_manager import ContextManager
from analysis_framework import AnalysisFramework

# Load context
context = ContextManager("nimrodfisher", "workshop-queries-repo")
context.load_schema_from_github("schema.yml")
context.add_user_context("What's our MRR by plan?")

# Map to schema
mapping = context.map_user_question_to_schema(context.user_context['question'])

# Use in analysis
framework = AnalysisFramework(schema_context=context.schema_context)
# ... continue with analysis
```

## Best Practices

1. **Start Simple**: Always begin with basic counts and checks
2. **Build Gradually**: Add complexity step by step
3. **Validate Aggregations**: Always validate when creating new segments
4. **Document Assumptions**: Be explicit about assumptions
5. **Ask for Clarifications**: Don't guess - ask when uncertain
6. **Check Performance**: Monitor execution times and table sizes
7. **Use Context**: Leverage schema definitions and synonyms

## Integration with Your Workflow

1. **Schema Files**: Keep `schema.yml` in your GitHub repo
2. **Context Mapping**: Create context mapping files for complex analyses
3. **Analysis in Cursor**: Run analysis directly in Cursor chat
4. **HTML Dashboards**: Request dashboards when needed - generates HTML mockups

## Workflow in Cursor

1. **Ask a question**: "What's our MRR by plan?"
2. **Framework analyzes**: Runs transparent steps with validation
3. **See results**: Step-by-step output in chat
4. **Request dashboard**: "Create a dashboard for this"
5. **Get HTML file**: Open in browser to view

## Next Steps

1. Run `analysis_workflow_example.py` to see it in action
2. Use `analysis_runner.py` for analysis in Cursor
3. Request HTML dashboards when you need visualizations
4. Customize dashboard generator for your needs


# AI Workshop - Analysis Framework

A comprehensive analysis framework for data teams with performance-aware querying, validation, and HTML dashboard generation.

## Quick Start

```python
from analysis_framework import AnalysisFramework
from context_manager import ContextManager

# Initialize
context = ContextManager("nimrodfisher", "workshop-queries-repo")
context.load_schema_from_github("schema.yml")
framework = AnalysisFramework(schema_context=context.schema_context)
framework.connect()

# Run analysis
framework.run_sanity_checks("users")
framework.run_eda("users")
# ... continue with analysis

framework.close()
```

## Analysis Flow

**Follow the execution order defined in `ANALYSIS_FLOW.md`:**

1. **Phase 1: Sanity Checks** → Uses `sanity_check_rules.yml`
2. **Phase 2: EDA** → Uses `eda_rules.yml`
3. **Phase 3: Main Analysis** → Uses `schema.yml` (GitHub)
4. **Phase 4: Text Classification** → Uses user context (if needed)
5. **Phase 5: Diagnostic Analysis** → Uses analysis results (if relevant)

📖 **See `ANALYSIS_FLOW.md` for complete execution guide**  
🤖 **See `AGENT_INSTRUCTIONS.md` for agent-specific instructions**

## Key Features

- ✅ **Performance-Aware**: Optimizes queries based on table metadata
- ✅ **Validation**: Validates aggregations against raw data
- ✅ **Transparent**: Step-by-step explanations
- ✅ **Context-Aware**: Combines schema + user input + real-time data
- ✅ **Sanity Checks**: Data quality validation
- ✅ **EDA**: Exploratory data analysis
- ✅ **Text Classification**: LLM-based categorization
- ✅ **Diagnostic Analysis**: Segment comparison and insights

## Rule Files

| File | Phase | Purpose |
|------|-------|---------|
| `sanity_check_rules.yml` | 1 | Data quality checks |
| `eda_rules.yml` | 2 | Exploratory analysis |
| `schema.yml` (GitHub) | 3 | Schema context |
| User context | 4 | Text classification |
| Analysis results | 5 | Segment comparison |

## Documentation

- **`ANALYSIS_FLOW.md`** - Complete analysis workflow and execution order
- **`AGENT_INSTRUCTIONS.md`** - Quick reference for agents
- **`CODE_GENERATION_STANDARDS.md`** - SQL and Python code documentation standards
- **`SQL_OUTPUT_STANDARDS.md`** - **SQL output format requirements after execution**
- **`README_ANALYSIS_FRAMEWORK.md`** - Detailed framework documentation
- **`NEW_FEATURES.md`** - Guide to new features
- **`USAGE_GUIDE.md`** - Usage examples

## Installation

```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.8+
- PostgreSQL/Supabase connection
- Access to GitHub repo with schema.yml

## License

MIT

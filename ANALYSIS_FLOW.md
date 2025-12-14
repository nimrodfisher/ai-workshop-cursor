# Analysis Flow - Agent Execution Guide

This document defines the **correct sequence of actions** and **order of using rule files** for the analysis framework. Follow this flow step-by-step.

## Overview

The analysis follows a **5-phase sequential workflow**. Each phase has its own rule file and specific outputs that inform the next phase.

```
Phase 1: Sanity Checks → Phase 2: EDA → Phase 3: Main Analysis → Phase 4: Text Classification (if needed) → Phase 5: Diagnostic Analysis
```

---

## Phase 1: Sanity Checks

**Rule File:** `sanity_check_rules.yml`  
**Module:** `sanity_checker.py`  
**Purpose:** Validate data quality before analysis

### Execution Order:

1. **Identify relevant tables** from the user's question
2. **Load rules** from `sanity_check_rules.yml`
3. **Run sanity checks** on each relevant table:
   ```python
   framework.run_sanity_checks("table_name")
   ```
4. **Review results** - Check for errors/warnings
5. **Decide next step:**
   - If **errors found**: Report to user, may need data cleaning
   - If **warnings only**: Proceed with caution
   - If **all passed**: Continue to Phase 2

### Rule File Structure:
- `sanity_checks.null_checks` - Null value validation
- `sanity_checks.duplicate_checks` - Duplicate detection
- `sanity_checks.consistency_checks` - Data consistency
- `sanity_checks.completeness_checks` - Data completeness
- `table_specific_rules` - Table-specific configurations

### Output:
- Data quality report
- List of issues (errors/warnings/info)
- Decision: proceed or stop

---

## Phase 2: EDA (Exploratory Data Analysis)

**Rule File:** `eda_rules.yml`  
**Module:** `eda_analyzer.py`  
**Purpose:** Understand data distributions, patterns, and relationships

### Execution Order:

1. **Load rules** from `eda_rules.yml`
2. **Run EDA** on relevant tables:
   ```python
   framework.run_eda("table_name", sample_size=1000)
   ```
3. **Review EDA results:**
   - Basic statistics
   - Distribution analysis
   - Relationship analysis
   - Time-series analysis (if applicable)
4. **Check flags** - Review any issues raised
5. **Review typical questions** - Address user's likely questions
6. **Proceed to Phase 3** with data understanding

### Rule File Structure:
- `eda_phases.basic_stats` - Descriptive statistics
- `eda_phases.distribution_analysis` - Distribution checks
- `eda_phases.relationship_analysis` - Correlation analysis
- `eda_phases.time_series_analysis` - Temporal patterns
- `typical_questions` - Questions to flag

### Output:
- Statistical summary
- Distribution information
- Flags and warnings
- Typical questions list
- Data understanding for next phase

---

## Phase 3: Main Analysis

**Rule File:** None (uses schema context from GitHub)  
**Code Standards:** `CODE_GENERATION_STANDARDS.md`  
**Module:** `analysis_framework.py`  
**Purpose:** Execute the actual analysis queries

### Execution Order:

1. **Load schema context** from GitHub repo (`schema.yml`)
2. **Map user question** to schema elements
3. **Build queries** step-by-step:
   - Start simple (counts)
   - Add filters
   - Add aggregations
   - Add joins
4. **Document queries** with:
   - Header comment block (purpose, context, flow)
   - CTE comments (purpose, logic, output)
   - Inline comments (complex logic)
   - Full flow explanation
5. **Execute each step** with validation:
   ```python
   framework.add_step(
       description="...",
       query="...",
       validate=True,  # If aggregation
       aggregation_column="...",
       segment_columns=["..."],
       table_name="..."
   )
   ```
6. **Validate aggregations** - Check 2-3 sample cases
7. **Report results** transparently

### Dependencies:
- Uses results from Phase 1 (sanity checks) - know data quality
- Uses results from Phase 2 (EDA) - understand distributions
- Uses `schema.yml` from GitHub - understand structure

### Output:
- Analysis results
- Validation reports
- Transparent step summaries
- Fully documented SQL/Python code

### Code Documentation Requirements:
- ✅ Header comment block with purpose, context, and flow
- ✅ CTE documentation (purpose, input, transformation, output)
- ✅ Inline comments for complex logic
- ✅ Complete flow explanation
- ✅ Assumptions documented
- ✅ See `CODE_GENERATION_STANDARDS.md` for templates

### SQL Output Requirements (After Execution):
- ✅ **Simple explanation** in plain language (1-2 sentences)
- ✅ **Formatted SQL code** with proper indentation
- ✅ **All comments preserved** from the query
- ✅ **Results summary** or formatted table
- ✅ See `SQL_OUTPUT_STANDARDS.md` for complete format requirements

---

## Phase 4: Text Classification (Conditional)

**Rule File:** None (uses user context)  
**Module:** `text_classifier.py`  
**Purpose:** Classify text data when needed

### Execution Order:

1. **Check if needed:**
   - Does user question involve text classification?
   - Are there text columns that need categorization?
2. **If needed:**
   ```python
   framework.classify_text_column(
       table_name="...",
       column_name="...",
       user_context="user's context for classification",
       num_categories=5
   )
   ```
3. **Review categories** - Are they appropriate?
4. **Apply classification** to data
5. **Analyze classified data**
6. **Return to Phase 3** or proceed to Phase 5

### When to Use:
- User explicitly requests classification
- Text data needs to be grouped/categorized
- Analysis requires new text-based segments

### Output:
- Classification categories
- Mapped data
- Ready for analysis

---

## Phase 5: Diagnostic Analysis & Segment Comparison

**Rule File:** None (uses analysis results)  
**Module:** `diagnostic_analyzer.py`  
**Purpose:** Compare segments and generate insights

### Execution Order:

1. **Check if relevant:**
   - Does analysis involve segments?
   - Are comparisons needed?
2. **If relevant:**
   ```python
   framework.run_diagnostic_analysis(
       query="SELECT ...",
       target_column="metric_to_compare",
       segment_columns=["segment1", "segment2"],
       description="..."
   )
   ```
3. **Review comparisons:**
   - Segment statistics
   - Statistical significance
   - Performance gaps
4. **Generate insights** automatically
5. **Report findings**

### When to Use:
- Comparing groups/segments
- Identifying performance differences
- Statistical significance testing needed

### Output:
- Segment comparisons
- Statistical tests
- Performance gaps
- Insights

---

## Complete Flow Diagram

```
START
  │
  ├─→ Phase 1: Sanity Checks
  │   └─→ Use: sanity_check_rules.yml
  │   └─→ Output: Data quality report
  │
  ├─→ Phase 2: EDA
  │   └─→ Use: eda_rules.yml
  │   └─→ Output: Data understanding
  │
  ├─→ Phase 3: Main Analysis
  │   └─→ Use: schema.yml (from GitHub)
  │   └─→ Output: Analysis results
  │
  ├─→ Phase 4: Text Classification (if needed)
  │   └─→ Use: User context
  │   └─→ Output: Classified data
  │
  └─→ Phase 5: Diagnostic Analysis (if relevant)
      └─→ Use: Analysis results
      └─→ Output: Insights and comparisons
```

---

## Rule File Reference

| Phase | Rule File | Purpose | When to Use |
|-------|-----------|---------|-------------|
| 1 | `sanity_check_rules.yml` | Data quality checks | Always - first step |
| 2 | `eda_rules.yml` | Exploratory analysis | Always - after sanity checks |
| 3 | `schema.yml` (GitHub) | Schema context | Always - for query building |
| 4 | User context | Text classification | Only if text classification needed |
| 5 | Analysis results | Segment comparison | Only if segments need comparison |

---

## Agent Execution Checklist

### Before Starting:
- [ ] Load `sanity_check_rules.yml`
- [ ] Load `eda_rules.yml`
- [ ] Load schema from GitHub (`schema.yml`)
- [ ] Understand user's question

### Phase 1: Sanity Checks
- [ ] Identify relevant tables
- [ ] Run sanity checks on each table
- [ ] Review results
- [ ] Report issues to user
- [ ] Decide: proceed or stop

### Phase 2: EDA
- [ ] Run EDA on relevant tables
- [ ] Review statistics
- [ ] Check flags
- [ ] Address typical questions
- [ ] Document findings

### Phase 3: Main Analysis
- [ ] Map question to schema
- [ ] Build queries step-by-step
- [ ] Execute with validation
- [ ] Report transparently

### Phase 4: Text Classification (if needed)
- [ ] Determine if needed
- [ ] Get user context
- [ ] Classify text column
- [ ] Review categories
- [ ] Apply to data

### Phase 5: Diagnostic Analysis (if relevant)
- [ ] Determine if relevant
- [ ] Run segment comparison
- [ ] Review statistical tests
- [ ] Generate insights
- [ ] Report findings

---

## Example: Complete Workflow

```python
from analysis_framework import AnalysisFramework
from context_manager import ContextManager

# Initialize
context = ContextManager("nimrodfisher", "workshop-queries-repo")
context.load_schema_from_github("schema.yml")
framework = AnalysisFramework(schema_context=context.schema_context)
framework.connect()

# PHASE 1: Sanity Checks (uses sanity_check_rules.yml)
framework.run_sanity_checks("users")
framework.run_sanity_checks("subscriptions")

# PHASE 2: EDA (uses eda_rules.yml)
framework.run_eda("users", sample_size=1000)
framework.run_eda("subscriptions", sample_size=1000)

# PHASE 3: Main Analysis (uses schema.yml from GitHub)
step = framework.add_step(
    description="Calculate MRR by plan",
    query="SELECT plan, SUM(monthly_price) as mrr FROM ...",
    validate=True,
    aggregation_column="mrr",
    segment_columns=["plan"],
    table_name="subscriptions"
)

# PHASE 4: Text Classification (if needed)
# classification = framework.classify_text_column(...)

# PHASE 5: Diagnostic Analysis (if relevant)
diagnostic = framework.run_diagnostic_analysis(
    query="SELECT plan, monthly_price FROM subscriptions...",
    target_column="monthly_price",
    segment_columns=["plan"]
)

framework.close()
```

---

## Important Notes

1. **Sequential Execution**: Phases must be executed in order (1 → 2 → 3 → 4 → 5)
2. **Conditional Phases**: Phase 4 and 5 are optional - only run if needed
3. **Rule File Loading**: Load rule files at the start of each phase
4. **Context Preservation**: Results from earlier phases inform later phases
5. **Transparency**: Always explain what you're doing and why

---

## Customization

### Modify Rule Files:
- **`sanity_check_rules.yml`**: Adjust data quality thresholds
- **`eda_rules.yml`**: Customize EDA checks and flags
- **`schema.yml`** (GitHub): Update schema definitions

### Skip Phases (if appropriate):
- Can skip Phase 4 if no text classification needed
- Can skip Phase 5 if no segment comparison needed
- **Never skip Phase 1 or 2** - they provide essential context

---

## Troubleshooting

**Issue**: Sanity checks fail  
**Action**: Report to user, may need data cleaning before proceeding

**Issue**: EDA shows unexpected patterns  
**Action**: Flag for user, adjust analysis accordingly

**Issue**: Text classification categories don't make sense  
**Action**: Ask user for clarification on context

**Issue**: Diagnostic analysis shows no significant differences  
**Action**: Report this finding - it's still valuable information


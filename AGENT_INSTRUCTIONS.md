# Agent Instructions - Analysis Framework Execution

## Quick Reference: Rule Files and Execution Order

### Rule Files Location:
1. `sanity_check_rules.yml` - Phase 1
2. `eda_rules.yml` - Phase 2
3. `schema.yml` (GitHub) - Phase 3
4. User context - Phase 4 (if needed)
5. Analysis results - Phase 5 (if relevant)

### Execution Sequence:

```
1. SANITY CHECKS (sanity_check_rules.yml)
   ↓
2. EDA (eda_rules.yml)
   ↓
3. MAIN ANALYSIS (schema.yml from GitHub)
   ↓
4. TEXT CLASSIFICATION (if needed - user context)
   ↓
5. DIAGNOSTIC ANALYSIS (if relevant - analysis results)
```

---

## Step-by-Step Execution Guide

### STEP 1: Initialize and Load Rules

```python
# Load context
context = ContextManager("nimrodfisher", "workshop-queries-repo")
context.load_schema_from_github("schema.yml")

# Initialize framework
framework = AnalysisFramework(schema_context=context.schema_context)
framework.connect()
```

**Rule Files to Load:**
- ✅ `sanity_check_rules.yml` (automatically loaded by SanityChecker)
- ✅ `eda_rules.yml` (automatically loaded by EDAAnalyzer)
- ✅ `schema.yml` (loaded from GitHub)

---

### STEP 2: Phase 1 - Sanity Checks

**Rule File:** `sanity_check_rules.yml`

**What to Do:**
1. Identify tables from user's question
2. Run sanity checks on each table
3. Review results
4. Report issues

**Code:**
```python
# For each relevant table
framework.run_sanity_checks("table_name")
```

**Check These Sections in Rule File:**
- `sanity_checks.null_checks` - Null validation rules
- `sanity_checks.duplicate_checks` - Duplicate detection rules
- `sanity_checks.consistency_checks` - Consistency validation rules
- `sanity_checks.completeness_checks` - Completeness rules
- `table_specific_rules.{table_name}` - Table-specific rules

**Decision Point:**
- Errors found → Report to user, may need to stop
- Warnings only → Proceed with caution
- All passed → Continue to Phase 2

---

### STEP 3: Phase 2 - EDA

**Rule File:** `eda_rules.yml`

**What to Do:**
1. Run EDA on relevant tables
2. Review statistics and distributions
3. Check flags
4. Address typical questions

**Code:**
```python
# For each relevant table
framework.run_eda("table_name", sample_size=1000)
```

**Check These Sections in Rule File:**
- `eda_phases.basic_stats` - What statistics to calculate
- `eda_phases.distribution_analysis` - Distribution checks
- `eda_phases.relationship_analysis` - Correlation analysis
- `eda_phases.time_series_analysis` - Temporal patterns
- `typical_questions` - Questions to flag

**Output to Review:**
- Basic statistics
- Distribution flags
- Correlation warnings
- Typical questions list

---

### STEP 4: Phase 3 - Main Analysis

**Rule File:** `schema.yml` (from GitHub)

**What to Do:**
1. Map user question to schema
2. Build queries step-by-step
3. Execute with validation
4. Report transparently

**Code:**
```python
# Build analysis step-by-step
framework.add_step(
    description="...",
    query="...",
    assumptions=[...],
    clarifications=[...],
    validate=True,  # If aggregation
    aggregation_column="...",
    segment_columns=["..."],
    table_name="..."
)
```

**Use Schema Context:**
- `models` - Table definitions
- `relationships` - Foreign key relationships
- `common_business_questions` - Query patterns
- `common_metrics` - Metric definitions

**Validation:**
- Always validate aggregations
- Check 2-3 sample cases
- Report validation results

---

### STEP 5: Phase 4 - Text Classification (Conditional)

**Rule File:** User context (no file, use user input)

**When to Use:**
- User asks for text classification
- Text columns need categorization
- New text-based segments needed

**What to Do:**
1. Determine if needed
2. Get user context for classification
3. Classify text column
4. Review categories
5. Apply to data

**Code:**
```python
if text_classification_needed:
    framework.classify_text_column(
        table_name="...",
        column_name="...",
        user_context="user's context",
        num_categories=5
    )
```

**Decision Point:**
- Categories appropriate → Continue
- Categories need adjustment → Ask user

---

### STEP 6: Phase 5 - Diagnostic Analysis (Conditional)

**Rule File:** Analysis results (no file, use previous results)

**When to Use:**
- Comparing segments/groups
- Statistical significance needed
- Performance gaps to identify

**What to Do:**
1. Determine if relevant
2. Run segment comparison
3. Review statistical tests
4. Generate insights

**Code:**
```python
if segment_comparison_needed:
    framework.run_diagnostic_analysis(
        query="SELECT ...",
        target_column="metric",
        segment_columns=["segment1", "segment2"],
        description="..."
    )
```

**Output to Review:**
- Segment statistics
- Statistical significance (p-values)
- Performance gaps
- Generated insights

---

## Decision Tree

```
START
│
├─→ Load all rule files
│
├─→ Phase 1: Sanity Checks
│   ├─→ Errors? → Report, may stop
│   └─→ Continue
│
├─→ Phase 2: EDA
│   └─→ Document findings
│
├─→ Phase 3: Main Analysis
│   └─→ Execute queries
│
├─→ Text classification needed?
│   ├─→ Yes → Phase 4
│   └─→ No → Skip
│
└─→ Segment comparison needed?
    ├─→ Yes → Phase 5
    └─→ No → Skip
```

---

## Rule File Sections Reference

### sanity_check_rules.yml
```yaml
sanity_checks:
  null_checks: # Check for nulls
  duplicate_checks: # Check for duplicates
  consistency_checks: # Check consistency
  completeness_checks: # Check completeness

table_specific_rules:
  {table_name}: # Table-specific rules
```

### eda_rules.yml
```yaml
eda_phases:
  basic_stats: # Basic statistics
  distribution_analysis: # Distributions
  relationship_analysis: # Relationships
  time_series_analysis: # Time patterns

typical_questions: # Questions to flag
```

### schema.yml (GitHub)
```yaml
models: # Table definitions
relationships: # Foreign keys
common_business_questions: # Query patterns
common_metrics: # Metric definitions
```

---

## Common Patterns

### Pattern 1: Simple Analysis
```
Phase 1 → Phase 2 → Phase 3 → Done
```

### Pattern 2: Analysis with Text
```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Done
```

### Pattern 3: Analysis with Comparison
```
Phase 1 → Phase 2 → Phase 3 → Phase 5 → Done
```

### Pattern 4: Complete Analysis
```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Done
```

---

## Error Handling

**Rule File Not Found:**
- Use default rules
- Warn user
- Continue with available rules

**Sanity Check Errors:**
- Report to user
- Ask if should proceed
- May need data cleaning

**EDA Flags:**
- Document flags
- Adjust analysis if needed
- Inform user

**Validation Failures:**
- Review raw data
- Check query logic
- Report to user

---

## Code Generation Standards

**CRITICAL: All SQL and Python code must follow documentation standards**

### SQL Code Requirements:

1. **Header Comment Block** - Must include:
   - Query purpose
   - Business context
   - Logic flow (step-by-step)
   - Assumptions
   - Output description

2. **CTE Documentation** - Each CTE must have:
   - Purpose statement
   - Input explanation
   - Transformation logic
   - Output description

3. **Inline Comments** - Explain:
   - Complex calculations
   - Join logic
   - Filter conditions
   - Aggregations

4. **Flow Explanation** - Document the complete flow from start to finish

**See `CODE_GENERATION_STANDARDS.md` for complete templates and examples**

### Python Code Requirements:

1. **Comprehensive Docstrings** - Must include:
   - Function purpose
   - Business context
   - Logic flow
   - Parameter documentation
   - Return value description
   - Assumptions
   - Example usage

2. **Inline Comments** - Explain:
   - Complex logic
   - Step-by-step transformations
   - Edge case handling
   - Business rules

3. **Flow Documentation** - Document the complete algorithm flow

**See `CODE_GENERATION_STANDARDS.md` for complete templates and examples**

## Best Practices

1. **Always follow sequence** - Don't skip phases 1-2
2. **Load rule files** at start of each phase
3. **Report transparently** - Explain what you're doing
4. **Validate aggregations** - Always validate when creating segments
5. **Use context** - Results from earlier phases inform later ones
6. **Ask for clarification** - When uncertain, ask user
7. **Document all code** - Follow `CODE_GENERATION_STANDARDS.md` strictly

---

## Quick Checklist

Before starting analysis:
- [ ] Load `sanity_check_rules.yml`
- [ ] Load `eda_rules.yml`
- [ ] Load `schema.yml` from GitHub
- [ ] Understand user's question

During analysis:
- [ ] Run Phase 1 (sanity checks)
- [ ] Run Phase 2 (EDA)
- [ ] Run Phase 3 (main analysis)
  - [ ] Document all SQL queries with header comments
  - [ ] Document all CTEs with purpose and logic
  - [ ] Add inline comments for complex logic
  - [ ] Explain complete flow
- [ ] Run Phase 4 (if text classification needed)
- [ ] Run Phase 5 (if segment comparison needed)

After analysis:
- [ ] Review all results
- [ ] Generate summary
- [ ] Report findings transparently


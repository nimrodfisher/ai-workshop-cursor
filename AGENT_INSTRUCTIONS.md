# Agent Instructions - Analysis Framework Execution

## ⚠️ MANDATORY WORKFLOW ORDER - READ FIRST ⚠️

**BEFORE writing ANY analysis queries, you MUST complete these phases IN ORDER:**

```
✅ Phase 0: Load schema.yml from GitHub (ALWAYS FIRST)
    ↓
✅ Phase 1: Run Sanity Checks on all relevant tables
    ↓
✅ Phase 2: Run EDA on all relevant tables
    ↓
🛑 CHECKPOINT 1: Present validation results, ask permission
    ↓
✅ Phase 3: Write and execute main analysis queries
    ↓
🛑 CHECKPOINT 2: Present analysis results
    ↓
✅ Phase 4: Synthesize conclusions
    ↓
🛑 CHECKPOINT 3: Ask before generating reports
    ↓
✅ Phase 5: Generate Branded Reports (MANDATORY FINAL STEP)
    ↓
✅ Phase 6: Create analysis_flow.md (MANDATORY FINAL STEP)
```

**🚫 NEVER jump straight to Phase 3 (main analysis queries)**
**🚫 NEVER skip Phases 1 and 2**
**🚫 NEVER deliver reports that do not follow branded styling guidelines**

If you catch yourself about to execute an analysis query before completing validation:
→ STOP
→ Go back to Phase 1
→ Complete the proper workflow

---

## Quick Reference: Rule Files and Execution Order

### Rule Files Location:
0. `schema.yml` (GitHub - MANDATORY FIRST) - Business Context (loaded via GitHub MCP)
1. `sanity_check_rules.yml` - Phase 1
2. `eda_rules.yml` - Phase 2
3. `html-reports.mdc` - Phase 5 (Branding & Styling)
4. `interactive_dashboard.mdc` - Phase 5 (Interactivity)
5. `pdf_reports.mdc` - Phase 5 (PDF Standards)
6. `analysis_flow_visualization.mdc` - Phase 6 (Visual Mind Map)

---

## Step-by-Step Execution Guide

### STEP 0: Load Schema Context (MANDATORY - ALWAYS FIRST)

**CRITICAL: This step is REQUIRED for EVERY analysis. No exceptions.**

Before any analysis begins, you MUST load the schema.yml file from GitHub using the GitHub MCP tool:

```
Use GitHub MCP tool: get_file_contents
Parameters:
  - owner: "nimrodfisher"
  - repo: "workshop-queries-repo"
  - path: "schema.yml"
```

**What This Provides:**
1. **Business Context**: Table descriptions, synonyms, business meanings
2. **Common Metrics**: Pre-defined calculations (MRR, Churn, ARPU, etc.)
3. **Common Questions**: Query patterns for frequent analysis types
4. **Relationships**: How tables join together
5. **SQL Style Guide**: Formatting standards to follow

---

### STEP 1: Initialize Analysis Context

After loading schema.yml, proceed with analysis setup:

**Rule Files to Reference:**
- ✅ `sanity_check_rules.yml` (for data validation)
- ✅ `eda_rules.yml` (for exploratory analysis)
- ✅ `schema.yml` (LOADED FROM GITHUB - business context)

---

### STEP 2: Phase 1 - Sanity Checks (MANDATORY)

**Rule File:** `sanity_check_rules.yml`

**Code:**
```python
framework.run_sanity_checks("table_name")
```

---

### STEP 3: Phase 2 - EDA (MANDATORY)

**Rule File:** `eda_rules.yml`

**Code:**
```python
framework.run_eda("table_name", sample_size=1000)
```

**CHECKPOINT 1: After Validation & EDA Completion**

---

### STEP 4: Phase 3 - Main Analysis

**Business Context:** `schema.yml` (already loaded from GitHub in Step 0)

**Code:**
```python
framework.add_step(
    description="...",
    query="...",
    validate=True,
    table_name="..."
)
```

**CHECKPOINT 2: After First Query Execution**

---

### STEP 5: Phase 4 - Synthesis & Conclusions

**What to Do:**
1. Review all query results and EDA findings.
2. Synthesize key insights into `conclusions/conclusions.md`.
3. Ensure all business questions are answered.

**CHECKPOINT 3: Before Generating Deliverables**

#### Pre-Report Generation Validation

**CRITICAL: Before generating ANY reports, verify the following checklist:**

- [ ] `deliverables/` folder exists in analysis directory (create if missing)
- [ ] All query results are saved in `data/` folder as JSON files
- [ ] `conclusions/conclusions.md` is complete with findings and recommendations
- [ ] `analysis_flow.md` exists and documents the analysis workflow
- [ ] All queries in `queries/` folder are properly documented with headers

**⚠️ If ANY checklist item fails, STOP and complete it before proceeding with report generation.**

**Folder Structure Check:**
```
analyses/{YYYY-MM-DD}_{analysis_slug}/
├── deliverables/          ← Must exist before generating reports
├── data/                  ← Must contain query results (*.json)
├── queries/               ← Must contain documented SQL files
├── conclusions/
│   └── conclusions.md     ← Must be complete
└── analysis_flow.md       ← Must exist
```

---

### STEP 6: Phase 5 - Report Generation (MANDATORY FINAL STEP)

**CRITICAL: All generated reports (HTML, PDF) MUST adhere to the styling guidelines.**

**Rule Files:**
- ✅ [.cursor/rules/html-reports.mdc](.cursor/rules/html-reports.mdc) (Branding & HTML Technicals)
- ✅ [.cursor/rules/pdf_reports.mdc](.cursor/rules/pdf_reports.mdc) (PDF & ReportLab Technicals)
- ✅ [.cursor/rules/interactive_dashboard.mdc](.cursor/rules/interactive_dashboard.mdc) (Dashboard Interactivity)

**Key Requirements:**
1.  **Output Location (MANDATORY)**: ALL reports MUST be saved to the `deliverables/` folder:
    - Path: `analyses/{YYYY-MM-DD}_{analysis_slug}/deliverables/`
    - Static HTML: `deliverables/report.html`
    - Interactive Dashboard: `deliverables/report_interactive.html`
    - PDF Summary: `deliverables/report_summary.pdf`
    - **⚠️ Create the deliverables/ folder if it doesn't exist**
    - **❌ NEVER** use custom filenames like `bug_reporter_analysis_report.html`
    - **✅ ALWAYS** use standardized names: `report.html`, `report_interactive.html`, `report_summary.pdf`
2.  **Context-Aware Logic**: For EVERY analysis, create a custom Python generation script (e.g., `generate_branded_reports.py`). Never use generic templates.
3.  **Branding Consistency**:
    - **Author**: Nimrod Fisher | AI Analytics Hub
    - **Website**: ai-analytics-hub.com
    - **Profile Image**: Embed `.cursor/assets/photo.jpg` as base64.
4.  **PDF Formatting (MANDATORY)**:
    - Use `reportlab`.
    - ALWAYS wrap table cell content in `Paragraph` flowables to handle line breaks and bold tags.
    - Use a helper function like `p_wrap(text, style)` for consistency.
5.  **HTML Formatting**:
    - Use Bootstrap 5, DataTables.net, and ECharts/Plotly via CDN.
    - Follow the mandatory section sequence: Header → Executive Summary → Methodology → Findings → Recommendations → Footer.

---

### STEP 7: Phase 6 - Analysis Documentation

**Rule File:** [.cursor/rules/analysis_flow_visualization.mdc](.cursor/rules/analysis_flow_visualization.mdc)

**What to Do:**
1. Create `analysis_flow.md` in the analysis directory.
2. Include a visual mind map (Mermaid) documenting the actual steps taken.

---

## Code Generation Standards

**CRITICAL: All SQL and Python code must follow documentation standards in `CODE_GENERATION_STANDARDS.md`.**

### SQL Output Requirements (After Execution):

**MANDATORY: After executing any SQL query, you MUST output:**
1. **Simple Explanation** - Plain language description (1-2 sentences)
2. **Formatted SQL Code** - Properly indented with all comments preserved
3. **Results Summary** - Formatted results or summary

---

## Quick Checklist

Before starting analysis:
- [ ] **MANDATORY: Load `schema.yml` from GitHub using GitHub MCP tool**
- [ ] Reference `sanity_check_rules.yml` for validation
- [ ] Reference `eda_rules.yml` for exploratory analysis

After completing analysis:
- [ ] **MANDATORY: Create `analysis_flow.md` with visual mind map**

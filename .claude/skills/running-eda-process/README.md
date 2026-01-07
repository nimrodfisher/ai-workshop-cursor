# Running EDA Process Skill

**Version:** 1.0.0  
**Author:** Nimrod Fisher | AI Analytics Hub  
**Purpose:** Automates the mandatory Exploratory Data Analysis (EDA) workflow for data analysis projects

## Quick Start

This skill automatically activates when you mention:
- "Run EDA"
- "Perform exploratory analysis"
- "Validate data quality"
- "Run sanity checks"
- "Explore the data"

## What This Skill Does

The skill guides Claude through a rigorous 3-phase validation process that must be completed **before** any main analysis queries are written:

### Phase 0: Load Business Context
- Fetches `schema.yml` from GitHub for table definitions and metric formulas
- **Mandatory first step** - no analysis proceeds without business context

### Phase 1: Sanity Checks
- Validates data quality (nulls, duplicates, invalid values)
- Checks business logic (date validity, value ranges)
- Identifies data corruption or quality issues
- **Blocks analysis** if critical failures are found

### Phase 2: Exploratory Data Analysis
- Analyzes distributions (numeric, categorical, temporal)
- Detects outliers and patterns
- Validates join integrity for multi-table analysis
- Provides insights to guide query design

### Checkpoint 1: Approval Gate
- Presents validation summary with key findings
- **Waits for user approval** before proceeding
- Prevents wasted effort on bad data

## File Structure

```
running-eda-process/
├── SKILL.md                         # Main skill instructions (Claude reads this first)
├── VALIDATION_RULES_REFERENCE.md    # Detailed validation logic (loaded when needed)
├── EXAMPLES.md                      # Complete workflow examples (loaded when needed)
└── README.md                        # This file (human documentation)
```

## Progressive Disclosure

The skill uses **progressive disclosure** as recommended by Claude's official documentation:

- **SKILL.md** provides the overview and workflow steps
- **VALIDATION_RULES_REFERENCE.md** contains detailed SQL patterns (loaded only when Claude needs specifics)
- **EXAMPLES.md** shows complete end-to-end scenarios (loaded when user needs examples)

This keeps the initial context lean while providing deep knowledge when needed.

## Why This Skill Exists

### The Problem
Analysts often jump straight to queries without validating data, leading to:
- ❌ Wrong conclusions from bad data
- ❌ Hours wasted on invalid analysis
- ❌ Embarrassing errors in reports
- ❌ Lost trust with stakeholders

### The Solution
This skill **enforces** a validation-first approach:
- ✅ Data quality checked before analysis begins
- ✅ Surprises and anomalies caught early
- ✅ User approval required before heavy lifting
- ✅ Documented validation trail for reproducibility

## How It Works with Your Workflow

This skill integrates with your existing analysis framework:

1. **User asks analysis question** → Skill activates automatically
2. **Phase 0:** Loads schema.yml for business context
3. **Phase 1:** Runs `framework.run_sanity_checks("table_name")`
4. **Phase 2:** Runs `framework.run_eda("table_name")`
5. **Checkpoint 1:** Presents summary, waits for "yes" to proceed
6. **Main Analysis:** User-approved, proceeds to write queries

## Validation Standards

The skill applies industry-standard checks:

| Check Type | Examples | Severity |
|------------|----------|----------|
| **Data Quality** | Nulls, duplicates, orphans | 🚨 FAIL if >20% null |
| **Business Logic** | Dates, ranges, valid enums | 🚨 FAIL if impossible values |
| **Join Integrity** | Row count impact, coverage | ⚠️ WARNING if >5% change |
| **Statistical** | Distributions, outliers | ⚠️ WARNING if extreme |

## Example Usage

### Example 1: Single-Table Analysis

```
You: "Analyze monthly user signups"

Claude (using this skill):
1. Loads schema.yml from GitHub ✓
2. Runs sanity checks on users table ✓
3. Runs EDA on users table ✓
4. Presents: "Found 15,234 users from Jan 2023-Dec 2024.
   Data quality is excellent. Should I proceed with writing the query?"
   
You: "Yes"

Claude: Writes and executes signup trend query
```

### Example 2: Multi-Table Analysis

```
You: "Calculate revenue by customer tier"

Claude (using this skill):
1. Loads schema.yml (includes join relationships) ✓
2. Runs sanity checks on customers + subscriptions ✓
3. Validates join integrity (warns about 14 orphaned records) ✓
4. Runs EDA on both tables ✓
5. Presents: "Found 2,847 customers and 3,156 subscriptions.
   Join will exclude 14 orphaned records (0.4%). Should I proceed?"
   
You: "Yes"

Claude: Writes join query excluding orphans
```

## When Skill Triggers

The skill activates when Claude detects these patterns in your request:

**Direct triggers:**
- "Run EDA"
- "Perform exploratory analysis"
- "Validate the data"
- "Run sanity checks"

**Implicit triggers:**
- "Analyze [something]" → Skill knows analysis requires EDA first
- "Calculate [metric]" → Skill validates data before calculating
- "Compare [segments]" → Skill checks segment integrity first

## Customization

To modify validation thresholds, edit `VALIDATION_RULES_REFERENCE.md`:

```markdown
# Example: Change null threshold from 20% to 10%

**Severity Thresholds:**
- Nulls <10%: ✓ PASS
- Nulls 10-20%: ⚠️ WARNING
- Nulls >20%: 🚨 FAIL
```

## Integration with Other Skills

This skill works alongside:

- **SQL Query Standards Skill** - Formats queries after validation
- **Report Generation Skill** - Generates reports after analysis
- **Creating Skills Skill** - Meta: helps create new skills like this one

## Troubleshooting

### Skill not triggering?

Make sure your request includes trigger words:
- ❌ "Show me user data" (too vague)
- ✅ "Analyze user signups" (clear analysis intent)
- ✅ "Run EDA on users table" (explicit)

### Want to skip checkpoints?

Say: "Run the full analysis without stopping"
- Sets `SKIP_CHECKPOINTS = True`
- Skill still performs validation but doesn't pause

### Skill blocking on warnings?

By design - warnings require acknowledgment:
- Review the warning
- Decide if it's acceptable
- Respond "yes" to proceed or "no" to adjust

## Technical Details

**Skill Type:** Project Skill  
**Location:** `.claude/skills/running-eda-process/`  
**Applies to:** Anyone working in this repository  
**Dependencies:** 
- GitHub MCP (for schema.yml loading)
- Supabase MCP (for query execution)
- Analysis framework (`framework.run_sanity_checks()`, `framework.run_eda()`)

**Allowed Tools:** None restricted (uses standard permission model)

## References

- **Official Claude Skills Documentation:** https://code.claude.com/docs/en/skills
- **Project Validation Rules:** `.cursor/rules/data_validation_master.mdc`
- **Agent Workflow:** `agent_instructions.md`
- **Schema Repository:** https://github.com/nimrodfisher/workshop-queries-repo

## Version History

### 1.0.0 (2026-01-05)
- Initial release
- Implements mandatory 3-phase workflow (Schema → Sanity → EDA)
- Progressive disclosure with supporting reference files
- Complete examples for common analysis patterns
- Integration with conversational checkpoints

## Contributing

To improve this skill:

1. Edit `SKILL.md` for workflow changes
2. Edit `VALIDATION_RULES_REFERENCE.md` for validation logic
3. Edit `EXAMPLES.md` to add new scenarios
4. Test by asking Claude to run EDA on a sample table
5. Verify Checkpoint 1 presents correctly

## License

Internal use only - Nimrod Fisher | AI Analytics Hub




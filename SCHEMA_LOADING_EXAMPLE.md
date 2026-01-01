# How to Load Schema.yml in Every Analysis

## Overview

**MANDATORY FIRST STEP:** Every analysis must load schema.yml from GitHub using the GitHub MCP tool.

---

## Step-by-Step Process

### 1. Load Schema from GitHub (Always First)

Use the GitHub MCP tool to fetch the schema file:

```
Tool: user-github-get_file_contents
Parameters:
  owner: "nimrodfisher"
  repo: "workshop-queries-repo"
  path: "schema.yml"
```

**Expected Result:** Full schema.yml content with:
- Table definitions (`models`)
- Relationships (foreign keys)
- Common metrics (MRR, Churn, ARPU, etc.)
- Common business questions (query patterns)
- SQL style guide

---

### 2. Parse and Store Key Sections

After loading, extract these key sections:

#### A. Models (Tables)
```yaml
models:
  - name: subscriptions
    description: "Tracks which accounts are subscribed to which products"
    synonyms: ["plans", "memberships"]
    columns:
      - name: monthly_price
        description: "Agreed-upon monthly price"
        synonyms: ["price_monthly", "monthly_cost"]
```

**Use for:** Understanding what tables exist, their business meaning, and column synonyms

#### B. Common Metrics
```yaml
common_metrics:
  - name: "MRR (Monthly Recurring Revenue)"
    calculation: "SUM(monthly_price) WHERE status = 'active'"
  - name: "Churn Rate"
    calculation: "COUNT(canceled_at) / COUNT(*) WHERE status = 'canceled' or 'active'"
```

**Use for:** Standard metric calculations to ensure consistency

#### C. Relationships
```yaml
relationships:
  - from: subscriptions.org_id
    to: accounts.id
    type: many_to_one
```

**Use for:** Knowing how to join tables correctly

#### D. Common Business Questions
```yaml
common_business_questions:
  - question: "What is our MRR by subscription plan?"
    query_pattern: |
      SELECT 
        a.plan,
        SUM(s.monthly_price) as total_mrr
      FROM subscriptions s
      JOIN accounts a ON s.org_id = a.id
      WHERE s.status = 'active'
      GROUP BY a.plan;
```

**Use for:** Pre-built query patterns for frequent questions

#### E. SQL Style Guide
```yaml
sql_style_guide: |
  UPPERCASE: All SQL keywords (SELECT, FROM, WHERE)
  lowercase: All table and column names
  snake_case: For column names
```

**Use for:** Formatting all SQL queries consistently

---

## 3. Use Schema Throughout Analysis

### Example: User asks "What's our MRR by plan?"

**Step 0: Load Schema** ✓ (Always done first)

**Step 1: Check Common Business Questions**
```
Search schema.yml → common_business_questions
Find: "What is our MRR by subscription plan?"
Pattern exists! ✓
```

**Step 2: Check Common Metrics**
```
Search schema.yml → common_metrics
Find: "MRR (Monthly Recurring Revenue)"
Calculation: SUM(monthly_price) WHERE status = 'active'
Use this definition ✓
```

**Step 3: Check Models and Relationships**
```
Search schema.yml → models
Tables needed: subscriptions, accounts
Join: subscriptions.org_id → accounts.id
Column: accounts.plan (synonyms: tier, subscription_plan)
```

**Step 4: Build Query Using Schema Context**
```sql
-- Built using schema.yml context
SELECT 
  a.plan,                          -- From schema: accounts.plan
  SUM(s.monthly_price) AS total_mrr,  -- From schema: MRR definition
  COUNT(*) AS subscription_count
FROM subscriptions s               -- From schema: subscriptions table
INNER JOIN accounts a              -- From schema: relationship
  ON s.org_id = a.id
WHERE s.status = 'active'          -- From schema: MRR calculation filter
GROUP BY a.plan
ORDER BY total_mrr DESC;           -- Following sql_style_guide
```

---

## 4. Benefits of Using Schema

### ✅ Consistency
- Everyone uses same metric definitions
- MRR calculated the same way every time

### ✅ Business Context
- Understand what columns mean
- Use business-friendly synonyms

### ✅ Speed
- Don't reinvent queries
- Use pre-built patterns

### ✅ Accuracy
- Correct joins using documented relationships
- Follow proven query patterns

### ✅ Living Documentation
- Schema updates automatically reflected
- No stale documentation

---

## 5. Schema Checklist

Before writing any query:

- [ ] Schema.yml loaded from GitHub using MCP tool
- [ ] Checked `common_metrics` for metric definition
- [ ] Checked `models` for table/column descriptions
- [ ] Checked `relationships` for join patterns
- [ ] Checked `common_business_questions` for similar patterns
- [ ] Following `sql_style_guide` formatting rules

---

## 6. Error Prevention

### ❌ Common Mistakes

**Without Schema:**
```sql
-- Wrong: Guessing column names
SELECT plan_name, sum(price) as revenue
FROM subscription
WHERE active = true
```

**With Schema:**
```sql
-- Correct: Using schema definitions
SELECT 
  a.plan,                          -- Schema confirms: accounts.plan
  SUM(s.monthly_price) AS total_mrr  -- Schema defines MRR
FROM subscriptions s               -- Schema confirms: subscriptions (not subscription)
INNER JOIN accounts a ON s.org_id = a.id  -- Schema defines relationship
WHERE s.status = 'active'          -- Schema confirms: status = 'active'
GROUP BY a.plan;
```

---

## 7. Practical Implementation

### In Cursor Agent Mode

```markdown
User: "Analyze MRR by plan"

Agent Steps:
1. Call GitHub MCP: get_file_contents("schema.yml")
2. Parse schema content
3. Check common_business_questions → Find "MRR by plan" pattern
4. Check common_metrics → Get MRR definition
5. Check models → Confirm tables and columns
6. Build query using schema context
7. Execute and validate
8. Generate report
```

### Schema Reference During Analysis

Keep these sections handy:
```
Schema Loaded: ✓

Quick Reference:
- MRR = SUM(monthly_price) WHERE status = 'active'
- Join: subscriptions → accounts (on org_id = id)
- Available plans: Free, Pro, Enterprise
- SQL Style: UPPERCASE keywords, lowercase identifiers
```

---

## 8. Schema Version Control

Since schema.yml is in GitHub:
- ✅ Always current (pulled fresh each time)
- ✅ Version controlled (can see history)
- ✅ Team can update (collaborative)
- ✅ Changes tracked (commit history)

**This is why we use GitHub MCP instead of a static rule file!**

---

## Quick Command Reference

```
# Load Schema (Always First Step)
Tool: user-github-get_file_contents
Params: {owner: "nimrodfisher", repo: "workshop-queries-repo", path: "schema.yml"}

# List Available Branches (Optional)
Tool: user-github-list_commits
Params: {owner: "nimrodfisher", repo: "workshop-queries-repo"}

# Check Schema Updates (Optional)
Tool: user-github-list_commits
Params: {owner: "nimrodfisher", repo: "workshop-queries-repo", path: "schema.yml"}
```

---

## Remember

**Every analysis MUST start with:**
1. Load schema.yml from GitHub ← **MANDATORY**
2. Reference schema throughout analysis
3. Use schema definitions for consistency
4. Follow schema formatting guidelines

**No exceptions!**






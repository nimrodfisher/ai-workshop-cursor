# SQL Output Standards

## Overview

After executing any SQL query using `mcp_supabase_execute_sql`, you **MUST** output the SQL code in a clear, formatted, and well-documented manner.

## Required Output Format

### 1. Execute the Query
```python
mcp_supabase_execute_sql(query="...")
```

### 2. Output the SQL Code

After execution, you **MUST** display:

1. **Formatted SQL Code** - Properly indented and readable
2. **Comments** - All comments from the query preserved
3. **Simple Explanation** - Plain language description of what the query does
4. **Data Persistence** - Save results to the analysis `data/` folder as JSON

## Output Template

```
## Query Execution

**What this query does:**
[Simple 1-2 sentence explanation in plain language]

**SQL Code:**
```sql
[Formatted SQL with all comments]
```

**Results:**
[Results summary or table]
```

## Example Output

### Good Example:

```
## Query Execution

**What this query does:**
This query calculates the total Monthly Recurring Revenue (MRR) for each subscription plan by adding up all the monthly prices from active subscriptions, grouped by plan type.

**SQL Code:**
```sql
/*
 * QUERY PURPOSE: Calculate Monthly Recurring Revenue (MRR) by subscription plan
 * 
 * BUSINESS CONTEXT: 
 * Need to understand revenue distribution across different plan tiers
 * 
 * LOGIC FLOW:
 * 1. Filter subscriptions to active status only
 * 2. Join with accounts to get plan information
 * 3. Aggregate monthly_price by plan
 * 
 * ASSUMPTIONS:
 * - Only active subscriptions count
 * - monthly_price represents recurring revenue
 */

WITH active_subscriptions_with_plans AS (
    SELECT 
        s.id AS subscription_id,
        s.monthly_price,
        a.plan
    FROM subscriptions s
    INNER JOIN accounts a ON s.org_id = a.id
    WHERE s.status = 'active'
      AND a.plan IS NOT NULL
)

SELECT 
    plan,
    SUM(monthly_price) AS total_mrr,
    COUNT(*) AS subscription_count
FROM active_subscriptions_with_plans
GROUP BY plan
ORDER BY total_mrr DESC;
```

**Results:**
- Free plan: $2,971 MRR (29 subscriptions)
- Pro plan: $2,845 MRR (25 subscriptions)
- Enterprise plan: $2,526 MRR (24 subscriptions)
```

### Bad Example (What NOT to do):

```
Query executed. Results: [data]
```

## Formatting Requirements

### SQL Code Formatting:

1. **Indentation**: Use 2 or 4 spaces consistently
2. **Line Breaks**: Break long lines for readability
3. **Keywords**: UPPERCASE for SQL keywords (SELECT, FROM, WHERE, etc.)
4. **Identifiers**: lowercase for table/column names
5. **Comments**: Preserve all comments from the query
6. **CTEs**: Each CTE on separate lines with clear separation

### Example Formatting:

```sql
-- Good formatting
SELECT 
    plan,
    SUM(monthly_price) AS total_mrr,
    COUNT(*) AS subscription_count
FROM subscriptions s
INNER JOIN accounts a ON s.org_id = a.id
WHERE s.status = 'active'
  AND a.plan IS NOT NULL
GROUP BY plan
ORDER BY total_mrr DESC;

-- Bad formatting (don't do this)
SELECT plan, SUM(monthly_price) AS total_mrr, COUNT(*) AS subscription_count FROM subscriptions s INNER JOIN accounts a ON s.org_id = a.id WHERE s.status = 'active' AND a.plan IS NOT NULL GROUP BY plan ORDER BY total_mrr DESC;
```

## Simple Explanation Requirements

The explanation should:

1. **Be in plain language** - No technical jargon unless necessary
2. **Be concise** - 1-2 sentences maximum
3. **Explain the purpose** - What business question it answers
4. **Mention key filters** - What data is included/excluded
5. **State the output** - What the result represents

### Explanation Templates:

**For aggregations:**
"This query [action] by [grouping] to show [what it calculates]."

**For filters:**
"This query finds [what] where [condition]."

**For joins:**
"This query combines [table1] and [table2] to [purpose]."

**For CTEs:**
"This query [step 1], then [step 2], to finally [result]."

## Complete Output Checklist

After executing SQL, ensure you include:

- [ ] **Simple explanation** in plain language
- [ ] **Formatted SQL code** with proper indentation
- [ ] **All comments preserved** from the original query
- [ ] **Data persistence** - results saved to `data/` as JSON
- [ ] **Results summary** or formatted table
- [ ] **Code block** with SQL syntax highlighting
- [ ] **Clear separation** between explanation, code, and results

## Enforcement

**This is mandatory** - Every SQL execution must follow this format. No exceptions.

If you execute SQL without providing the formatted output, you must:
1. Re-execute the query
2. Provide the formatted SQL code
3. Include the simple explanation

## Integration with Analysis Framework

When using the analysis framework:

1. Execute query via `mcp_supabase_execute_sql`
2. Display formatted SQL with comments
3. Provide simple explanation
4. Show results
5. Continue with framework steps (validation, etc.)

This ensures transparency and allows users to:
- Understand what was executed
- Review the logic
- Reuse the query
- Learn from the analysis










/*
================================================================================
QUERY: Accounts Table - Sanity Check
================================================================================
Business Question: Is the accounts table data valid and complete?
Author: Nimrod Fisher
Created: 2026-01-07
Last Modified: 2026-01-07
-----
DESCRIPTION:
  Validates the accounts table for data quality issues including:
  - Null values in critical columns
  - Plan and industry value distributions
  - Account naming completeness

DEPENDENCIES:
  - public.accounts: Main table being validated

OUTPUT:
  - check_name: Name of the validation check (text)
  - status: PASS or FAIL (text)
  - issue_count: Number of records with issues (integer)
  - details: Description of findings (text)

NOTES:
  - This is part of Phase 1: Data Validation
  - Accounts with bug tickets will be analyzed in main phase
================================================================================
*/

-- Check 1: Total record count
SELECT 
    'Total Records' AS check_name,
    CASE WHEN COUNT(*) > 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Total accounts in table' AS details
FROM accounts

UNION ALL

-- Check 2: Null IDs
SELECT 
    'Null IDs' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Primary key (id) should never be null' AS details
FROM accounts
WHERE id IS NULL

UNION ALL

-- Check 3: Null account names
SELECT 
    'Null Names' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'WARNING' END AS status,
    COUNT(*) AS issue_count,
    'Accounts without a name' AS details
FROM accounts
WHERE name IS NULL OR TRIM(name) = ''

UNION ALL

-- Check 4: Null industry
SELECT 
    'Null Industry' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'WARNING' END AS status,
    COUNT(*) AS issue_count,
    'Accounts without industry classification' AS details
FROM accounts
WHERE industry IS NULL

UNION ALL

-- Check 5: Null plan
SELECT 
    'Null Plan' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'WARNING' END AS status,
    COUNT(*) AS issue_count,
    'Accounts without a plan tier assigned' AS details
FROM accounts
WHERE plan IS NULL

UNION ALL

-- Check 6: Null created_at
SELECT 
    'Null created_at' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Accounts without creation timestamp' AS details
FROM accounts
WHERE created_at IS NULL

UNION ALL

-- Check 7: Plan distribution
SELECT 
    'Plan Distribution' AS check_name,
    'INFO' AS status,
    COUNT(DISTINCT plan) AS issue_count,
    'Distinct plan tiers: ' || STRING_AGG(DISTINCT plan, ', ') AS details
FROM accounts
WHERE plan IS NOT NULL

UNION ALL

-- Check 8: Industry distribution
SELECT 
    'Industry Distribution' AS check_name,
    'INFO' AS status,
    COUNT(DISTINCT industry) AS issue_count,
    'Distinct industries: ' || STRING_AGG(DISTINCT industry, ', ') AS details
FROM accounts
WHERE industry IS NOT NULL

UNION ALL

-- Check 9: Date range validation
SELECT 
    'Date Range' AS check_name,
    'INFO' AS status,
    CAST(DATE_PART('day', MAX(created_at) - MIN(created_at)) AS INTEGER) AS issue_count,
    'Accounts created from ' || MIN(created_at)::date || ' to ' || MAX(created_at)::date AS details
FROM accounts

UNION ALL

-- Check 10: Duplicate account names
SELECT 
    'Duplicate Names' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'INFO' END AS status,
    COUNT(*) AS issue_count,
    'Number of duplicate account names' AS details
FROM (
    SELECT name, COUNT(*) as cnt
    FROM accounts
    WHERE name IS NOT NULL
    GROUP BY name
    HAVING COUNT(*) > 1
) dupes

ORDER BY check_name;


/*
================================================================================
QUERY: Users Table - Sanity Check
================================================================================
Business Question: Is the users table data valid and complete?
Author: Nimrod Fisher
Created: 2026-01-07
Last Modified: 2026-01-07
-----
DESCRIPTION:
  Validates the users table for data quality issues including:
  - Null values in critical columns
  - Invalid foreign key references to accounts
  - Email and name completeness
  - Role value distributions

DEPENDENCIES:
  - public.users: Main table being validated
  - public.accounts: For org_id foreign key validation

OUTPUT:
  - check_name: Name of the validation check (text)
  - status: PASS or FAIL (text)
  - issue_count: Number of records with issues (integer)
  - details: Description of findings (text)

NOTES:
  - This is part of Phase 1: Data Validation
  - Users who opened bug tickets will be analyzed in main phase
================================================================================
*/

-- Check 1: Total record count
SELECT 
    'Total Records' AS check_name,
    CASE WHEN COUNT(*) > 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Total users in table' AS details
FROM users

UNION ALL

-- Check 2: Null IDs
SELECT 
    'Null IDs' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Primary key (id) should never be null' AS details
FROM users
WHERE id IS NULL

UNION ALL

-- Check 3: Null org_id
SELECT 
    'Null org_id' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Foreign key org_id should not be null' AS details
FROM users
WHERE org_id IS NULL

UNION ALL

-- Check 4: Orphaned org_id references
SELECT 
    'Orphaned org_id' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Users with invalid org_id references' AS details
FROM users u
LEFT JOIN accounts a ON u.org_id = a.id
WHERE u.org_id IS NOT NULL AND a.id IS NULL

UNION ALL

-- Check 5: Null full_name
SELECT 
    'Null full_name' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'WARNING' END AS status,
    COUNT(*) AS issue_count,
    'Users without a full name' AS details
FROM users
WHERE full_name IS NULL OR TRIM(full_name) = ''

UNION ALL

-- Check 6: Null email
SELECT 
    'Null email' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'WARNING' END AS status,
    COUNT(*) AS issue_count,
    'Users without an email address' AS details
FROM users
WHERE email IS NULL OR TRIM(email) = ''

UNION ALL

-- Check 7: Null role
SELECT 
    'Null role' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'WARNING' END AS status,
    COUNT(*) AS issue_count,
    'Users without a role assigned' AS details
FROM users
WHERE role IS NULL

UNION ALL

-- Check 8: Null created_at
SELECT 
    'Null created_at' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Users without creation timestamp' AS details
FROM users
WHERE created_at IS NULL

UNION ALL

-- Check 9: Role distribution
SELECT 
    'Role Distribution' AS check_name,
    'INFO' AS status,
    COUNT(DISTINCT role) AS issue_count,
    'Distinct role values: ' || STRING_AGG(DISTINCT role, ', ') AS details
FROM users
WHERE role IS NOT NULL

UNION ALL

-- Check 10: Date range validation
SELECT 
    'Date Range' AS check_name,
    'INFO' AS status,
    CAST(DATE_PART('day', MAX(created_at) - MIN(created_at)) AS INTEGER) AS issue_count,
    'Users created from ' || MIN(created_at)::date || ' to ' || MAX(created_at)::date AS details
FROM users

UNION ALL

-- Check 11: Duplicate emails
SELECT 
    'Duplicate Emails' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'WARNING' END AS status,
    COUNT(*) AS issue_count,
    'Number of duplicate email addresses' AS details
FROM (
    SELECT email, COUNT(*) as cnt
    FROM users
    WHERE email IS NOT NULL
    GROUP BY email
    HAVING COUNT(*) > 1
) dupes

ORDER BY check_name;





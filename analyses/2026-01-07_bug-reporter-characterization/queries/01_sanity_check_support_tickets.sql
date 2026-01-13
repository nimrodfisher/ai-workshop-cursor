/*
================================================================================
QUERY: Support Tickets Table - Sanity Check
================================================================================
Business Question: Is the support_tickets table data valid and complete?
Author: Nimrod Fisher
Created: 2026-01-07
Last Modified: 2026-01-07
-----
DESCRIPTION:
  Validates the support_tickets table for data quality issues including:
  - Null values in critical columns
  - Invalid foreign key references
  - Temporal consistency (opened_at vs closed_at)
  - Category and status value distributions

DEPENDENCIES:
  - public.support_tickets: Main table being validated
  - public.accounts: For org_id foreign key validation
  - public.users: For opened_by foreign key validation

OUTPUT:
  - check_name: Name of the validation check (text)
  - status: PASS or FAIL (text)
  - issue_count: Number of records with issues (integer)
  - details: Description of findings (text)

NOTES:
  - This is part of Phase 1: Data Validation
  - Must complete before running any analysis queries
  - Bug tickets are identified by category = 'bug'
================================================================================
*/

-- Check 1: Record counts and basic structure
SELECT 
    'Total Records' AS check_name,
    CASE WHEN COUNT(*) > 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Total support tickets in table' AS details
FROM support_tickets

UNION ALL

-- Check 2: Bug ticket count
SELECT 
    'Bug Tickets Count' AS check_name,
    CASE WHEN COUNT(*) > 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Support tickets with category = bug' AS details
FROM support_tickets
WHERE category = 'bug'

UNION ALL

-- Check 3: Null values in ID (should be 0)
SELECT 
    'Null IDs' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Primary key (id) should never be null' AS details
FROM support_tickets
WHERE id IS NULL

UNION ALL

-- Check 4: Null values in org_id (critical foreign key)
SELECT 
    'Null org_id' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Foreign key org_id should not be null' AS details
FROM support_tickets
WHERE org_id IS NULL

UNION ALL

-- Check 5: Null values in opened_by (acceptable but should track)
SELECT 
    'Null opened_by' AS check_name,
    'INFO' AS status,
    COUNT(*) AS issue_count,
    'Tickets with no user attribution (system-generated)' AS details
FROM support_tickets
WHERE opened_by IS NULL

UNION ALL

-- Check 6: Orphaned org_id references
SELECT 
    'Orphaned org_id' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Support tickets with invalid org_id references' AS details
FROM support_tickets st
LEFT JOIN accounts a ON st.org_id = a.id
WHERE st.org_id IS NOT NULL AND a.id IS NULL

UNION ALL

-- Check 7: Orphaned opened_by references
SELECT 
    'Orphaned opened_by' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Support tickets with invalid opened_by user references' AS details
FROM support_tickets st
LEFT JOIN users u ON st.opened_by = u.id
WHERE st.opened_by IS NOT NULL AND u.id IS NULL

UNION ALL

-- Check 8: Null category values
SELECT 
    'Null category' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Tickets without a category assigned' AS details
FROM support_tickets
WHERE category IS NULL

UNION ALL

-- Check 9: Null status values
SELECT 
    'Null status' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Tickets without a status assigned' AS details
FROM support_tickets
WHERE status IS NULL

UNION ALL

-- Check 10: Null opened_at timestamps
SELECT 
    'Null opened_at' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Tickets without an opening timestamp' AS details
FROM support_tickets
WHERE opened_at IS NULL

UNION ALL

-- Check 11: Temporal consistency (closed_at before opened_at)
SELECT 
    'Invalid timestamps' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Tickets closed before they were opened' AS details
FROM support_tickets
WHERE closed_at IS NOT NULL 
  AND closed_at < opened_at

UNION ALL

-- Check 12: Category value distribution
SELECT 
    'Category Distribution' AS check_name,
    'INFO' AS status,
    COUNT(DISTINCT category) AS issue_count,
    'Distinct category values: ' || STRING_AGG(DISTINCT category, ', ') AS details
FROM support_tickets
WHERE category IS NOT NULL

UNION ALL

-- Check 13: Status value distribution
SELECT 
    'Status Distribution' AS check_name,
    'INFO' AS status,
    COUNT(DISTINCT status) AS issue_count,
    'Distinct status values: ' || STRING_AGG(DISTINCT status, ', ') AS details
FROM support_tickets
WHERE status IS NOT NULL

UNION ALL

-- Check 14: Date range validation
SELECT 
    'Date Range' AS check_name,
    'INFO' AS status,
    CAST(DATE_PART('day', MAX(opened_at) - MIN(opened_at)) AS INTEGER) AS issue_count,
    'Tickets span from ' || MIN(opened_at)::date || ' to ' || MAX(opened_at)::date AS details
FROM support_tickets

ORDER BY check_name;





/*
================================================================================
QUERY: Subscriptions Table - Sanity Check
================================================================================
Business Question: Is the subscriptions table data valid and complete?
Author: Nimrod Fisher
Created: 2026-01-07
Last Modified: 2026-01-07
-----
DESCRIPTION:
  Validates the subscriptions table for data quality issues including:
  - Null values in critical columns
  - Invalid foreign key references
  - Status and pricing validations
  - Temporal consistency

DEPENDENCIES:
  - public.subscriptions: Main table being validated
  - public.accounts: For org_id foreign key validation
  - public.products: For product_id reference validation

OUTPUT:
  - check_name: Name of the validation check (text)
  - status: PASS or FAIL (text)
  - issue_count: Number of records with issues (integer)
  - details: Description of findings (text)

NOTES:
  - This is part of Phase 1: Data Validation
  - Subscription patterns for bug ticket accounts will be analyzed in main phase
================================================================================
*/

-- Check 1: Total record count
SELECT 
    'Total Records' AS check_name,
    CASE WHEN COUNT(*) > 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Total subscriptions in table' AS details
FROM subscriptions

UNION ALL

-- Check 2: Null IDs
SELECT 
    'Null IDs' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Primary key (id) should never be null' AS details
FROM subscriptions
WHERE id IS NULL

UNION ALL

-- Check 3: Null org_id
SELECT 
    'Null org_id' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Foreign key org_id should not be null' AS details
FROM subscriptions
WHERE org_id IS NULL

UNION ALL

-- Check 4: Null product_id
SELECT 
    'Null product_id' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Foreign key product_id should not be null' AS details
FROM subscriptions
WHERE product_id IS NULL

UNION ALL

-- Check 5: Orphaned org_id references
SELECT 
    'Orphaned org_id' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Subscriptions with invalid org_id references' AS details
FROM subscriptions s
LEFT JOIN accounts a ON s.org_id = a.id
WHERE s.org_id IS NOT NULL AND a.id IS NULL

UNION ALL

-- Check 6: Orphaned product_id references
SELECT 
    'Orphaned product_id' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'WARNING' END AS status,
    COUNT(*) AS issue_count,
    'Subscriptions with invalid product_id references' AS details
FROM subscriptions s
LEFT JOIN products p ON s.product_id = p.id
WHERE s.product_id IS NOT NULL AND p.id IS NULL

UNION ALL

-- Check 7: Null status
SELECT 
    'Null status' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'WARNING' END AS status,
    COUNT(*) AS issue_count,
    'Subscriptions without status classification' AS details
FROM subscriptions
WHERE status IS NULL

UNION ALL

-- Check 8: Null started_at
SELECT 
    'Null started_at' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'WARNING' END AS status,
    COUNT(*) AS issue_count,
    'Subscriptions without start date' AS details
FROM subscriptions
WHERE started_at IS NULL

UNION ALL

-- Check 9: Null monthly_price
SELECT 
    'Null monthly_price' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'WARNING' END AS status,
    COUNT(*) AS issue_count,
    'Subscriptions without pricing information' AS details
FROM subscriptions
WHERE monthly_price IS NULL

UNION ALL

-- Check 10: Negative or zero prices
SELECT 
    'Invalid Prices' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'WARNING' END AS status,
    COUNT(*) AS issue_count,
    'Subscriptions with negative or zero monthly_price' AS details
FROM subscriptions
WHERE monthly_price <= 0

UNION ALL

-- Check 11: Temporal consistency (canceled before started)
SELECT 
    'Invalid Dates' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Subscriptions canceled before they started' AS details
FROM subscriptions
WHERE canceled_at IS NOT NULL 
  AND started_at IS NOT NULL
  AND canceled_at < started_at

UNION ALL

-- Check 12: Status distribution
SELECT 
    'Status Distribution' AS check_name,
    'INFO' AS status,
    COUNT(DISTINCT status) AS issue_count,
    'Distinct status values: ' || STRING_AGG(DISTINCT status, ', ') AS details
FROM subscriptions
WHERE status IS NOT NULL

UNION ALL

-- Check 13: Active subscriptions count
SELECT 
    'Active Subscriptions' AS check_name,
    'INFO' AS status,
    COUNT(*) AS issue_count,
    'Number of currently active subscriptions' AS details
FROM subscriptions
WHERE status = 'active'

UNION ALL

-- Check 14: Date range validation
SELECT 
    'Date Range' AS check_name,
    'INFO' AS status,
    CAST(DATE_PART('day', MAX(started_at) - MIN(started_at)) AS INTEGER) AS issue_count,
    'Subscriptions span from ' || MIN(started_at)::date || ' to ' || MAX(started_at)::date AS details
FROM subscriptions
WHERE started_at IS NOT NULL

ORDER BY check_name;





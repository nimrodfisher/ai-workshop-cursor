/*
================================================================================
QUERY: Events Table - Sanity Check
================================================================================
Business Question: Is the events table data valid and complete?
Author: Nimrod Fisher
Created: 2026-01-07
Last Modified: 2026-01-07
-----
DESCRIPTION:
  Validates the events table for data quality issues including:
  - Null values in critical columns
  - Invalid foreign key references
  - Event type distributions
  - Temporal data validation

DEPENDENCIES:
  - public.events: Main table being validated
  - public.accounts: For org_id foreign key validation
  - public.users: For user_id foreign key validation

OUTPUT:
  - check_name: Name of the validation check (text)
  - status: PASS or FAIL (text)
  - issue_count: Number of records with issues (integer)
  - details: Description of findings (text)

NOTES:
  - This is part of Phase 1: Data Validation
  - Event activity patterns will be analyzed in main phase
================================================================================
*/

-- Check 1: Total record count
SELECT 
    'Total Records' AS check_name,
    CASE WHEN COUNT(*) > 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Total events in table' AS details
FROM events

UNION ALL

-- Check 2: Null IDs
SELECT 
    'Null IDs' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Primary key (id) should never be null' AS details
FROM events
WHERE id IS NULL

UNION ALL

-- Check 3: Null org_id
SELECT 
    'Null org_id' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Foreign key org_id should not be null' AS details
FROM events
WHERE org_id IS NULL

UNION ALL

-- Check 4: Null user_id (acceptable - some events are system-level)
SELECT 
    'Null user_id' AS check_name,
    'INFO' AS status,
    COUNT(*) AS issue_count,
    'Events without user attribution (system events)' AS details
FROM events
WHERE user_id IS NULL

UNION ALL

-- Check 5: Orphaned org_id references
SELECT 
    'Orphaned org_id' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Events with invalid org_id references' AS details
FROM events e
LEFT JOIN accounts a ON e.org_id = a.id
WHERE e.org_id IS NOT NULL AND a.id IS NULL

UNION ALL

-- Check 6: Orphaned user_id references
SELECT 
    'Orphaned user_id' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Events with invalid user_id references' AS details
FROM events e
LEFT JOIN users u ON e.user_id = u.id
WHERE e.user_id IS NOT NULL AND u.id IS NULL

UNION ALL

-- Check 7: Null event_type
SELECT 
    'Null event_type' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Events without type classification' AS details
FROM events
WHERE event_type IS NULL

UNION ALL

-- Check 8: Null occurred_at
SELECT 
    'Null occurred_at' AS check_name,
    CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
    COUNT(*) AS issue_count,
    'Events without timestamp' AS details
FROM events
WHERE occurred_at IS NULL

UNION ALL

-- Check 9: Event type distribution
SELECT 
    'Event Type Count' AS check_name,
    'INFO' AS status,
    COUNT(DISTINCT event_type) AS issue_count,
    'Number of distinct event types in system' AS details
FROM events
WHERE event_type IS NOT NULL

UNION ALL

-- Check 10: Date range validation
SELECT 
    'Date Range' AS check_name,
    'INFO' AS status,
    CAST(DATE_PART('day', MAX(occurred_at) - MIN(occurred_at)) AS INTEGER) AS issue_count,
    'Events span from ' || MIN(occurred_at)::date || ' to ' || MAX(occurred_at)::date AS details
FROM events

UNION ALL

-- Check 11: Events per user coverage
SELECT 
    'User Coverage' AS check_name,
    'INFO' AS status,
    COUNT(DISTINCT user_id) AS issue_count,
    'Number of unique users with at least one event' AS details
FROM events
WHERE user_id IS NOT NULL

UNION ALL

-- Check 12: Props data completeness
SELECT 
    'Null Props' AS check_name,
    'INFO' AS status,
    COUNT(*) AS issue_count,
    'Events without props metadata' AS details
FROM events
WHERE props IS NULL

ORDER BY check_name;


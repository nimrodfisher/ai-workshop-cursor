/*
================================================================================
QUERY: User-Level Bug Reporter vs Non-Reporter Comparison
================================================================================
Business Question: What characterizes individual users who report bugs vs. those who don't?
Author: AI Analytics
Created: 2026-01-07
Last Modified: 2026-01-07
-----
DESCRIPTION:
  Compares users who have opened bug tickets against users who haven't across
  demographic (role, plan tier, tenure) and behavioral (event activity, engagement)
  dimensions to identify what differentiates bug reporters.

DEPENDENCIES:
  - support_tickets: To identify bug reporters (category = 'bug')
  - users: For user demographic information
  - accounts: For account plan tier information
  - events: For user behavioral/engagement metrics

OUTPUT:
  - cohort: 'Bug Reporter' or 'Non-Bug Reporter'
  - user_count: Number of users in each cohort
  - avg_account_tenure_days: Average days since account creation
  - role_breakdown: JSON with role distribution
  - plan_breakdown: JSON with plan distribution
  - total_events: Total events across cohort
  - avg_events_per_user: Average events per user
  - median_events_per_user: Median events per user
  - event_diversity: Average unique event types per user
  - top_event_types: Most common event types

NOTES:
  - Bug tickets are identified by category = 'bug'
  - Non-bug reporters include all users who haven't opened bug tickets
  - Users with no events are included (0 event count)
  - Account tenure calculated from account.created_at to today
================================================================================
*/

WITH bug_reporters AS (
    -- Identify users who have opened at least one bug ticket
    SELECT DISTINCT 
        opened_by as user_id
    FROM support_tickets
    WHERE category = 'bug'
        AND opened_by IS NOT NULL
),

user_cohorts AS (
    -- Assign each user to a cohort
    SELECT 
        u.id as user_id,
        u.role,
        u.created_at as user_created_at,
        a.plan,
        a.created_at as account_created_at,
        CASE 
            WHEN br.user_id IS NOT NULL THEN 'Bug Reporter'
            ELSE 'Non-Bug Reporter'
        END as cohort
    FROM users u
    LEFT JOIN bug_reporters br ON u.id = br.user_id
    LEFT JOIN accounts a ON u.org_id = a.id
),

user_event_metrics AS (
    -- Calculate event metrics for each user
    SELECT 
        uc.user_id,
        uc.cohort,
        uc.role,
        uc.plan,
        EXTRACT(EPOCH FROM (NOW() - uc.account_created_at)) / 86400 as account_tenure_days,
        COUNT(e.id) as event_count,
        COUNT(DISTINCT e.event_type) as unique_event_types,
        STRING_AGG(DISTINCT e.event_type, ', ' ORDER BY e.event_type) as event_types_used
    FROM user_cohorts uc
    LEFT JOIN events e ON uc.user_id = e.user_id
    GROUP BY uc.user_id, uc.cohort, uc.role, uc.plan, uc.account_created_at
),

cohort_aggregates AS (
    -- Aggregate metrics by cohort
    SELECT 
        cohort,
        COUNT(*) as user_count,
        ROUND(AVG(account_tenure_days), 2) as avg_account_tenure_days,
        ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY account_tenure_days), 2) as median_account_tenure_days,
        SUM(event_count) as total_events,
        ROUND(AVG(event_count), 2) as avg_events_per_user,
        ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY event_count), 2) as median_events_per_user,
        ROUND(AVG(unique_event_types), 2) as avg_event_diversity,
        MAX(event_count) as max_events_per_user,
        MIN(event_count) as min_events_per_user
    FROM user_event_metrics
    GROUP BY cohort
),

role_breakdown AS (
    -- Calculate role distribution by cohort
    SELECT 
        cohort,
        JSONB_OBJECT_AGG(
            role, 
            JSONB_BUILD_OBJECT(
                'count', role_count,
                'percentage', ROUND(100.0 * role_count / total_users, 2)
            )
        ) as role_distribution
    FROM (
        SELECT 
            cohort,
            role,
            COUNT(*) as role_count,
            SUM(COUNT(*)) OVER (PARTITION BY cohort) as total_users
        FROM user_event_metrics
        GROUP BY cohort, role
    ) role_counts
    GROUP BY cohort
),

plan_breakdown AS (
    -- Calculate plan distribution by cohort
    SELECT 
        cohort,
        JSONB_OBJECT_AGG(
            plan, 
            JSONB_BUILD_OBJECT(
                'count', plan_count,
                'percentage', ROUND(100.0 * plan_count / total_users, 2)
            )
        ) as plan_distribution
    FROM (
        SELECT 
            cohort,
            plan,
            COUNT(*) as plan_count,
            SUM(COUNT(*)) OVER (PARTITION BY cohort) as total_users
        FROM user_event_metrics
        WHERE plan IS NOT NULL
        GROUP BY cohort, plan
    ) plan_counts
    GROUP BY cohort
),

event_type_breakdown AS (
    -- Get top event types by cohort
    SELECT 
        cohort,
        JSONB_AGG(
            JSONB_BUILD_OBJECT(
                'event_type', event_type,
                'count', event_count,
                'user_count', user_count
            ) ORDER BY event_count DESC
        ) as top_event_types
    FROM (
        SELECT 
            uem.cohort,
            e.event_type,
            COUNT(e.id) as event_count,
            COUNT(DISTINCT e.user_id) as user_count
        FROM user_event_metrics uem
        LEFT JOIN events e ON uem.user_id = e.user_id
        WHERE e.event_type IS NOT NULL
        GROUP BY uem.cohort, e.event_type
    ) event_counts
    GROUP BY cohort
)

-- Final output: Combine all metrics
SELECT 
    ca.cohort,
    ca.user_count,
    ca.avg_account_tenure_days,
    ca.median_account_tenure_days,
    ca.total_events,
    ca.avg_events_per_user,
    ca.median_events_per_user,
    ca.avg_event_diversity,
    ca.max_events_per_user,
    ca.min_events_per_user,
    rb.role_distribution,
    pb.plan_distribution,
    etb.top_event_types
FROM cohort_aggregates ca
LEFT JOIN role_breakdown rb ON ca.cohort = rb.cohort
LEFT JOIN plan_breakdown pb ON ca.cohort = pb.cohort
LEFT JOIN event_type_breakdown etb ON ca.cohort = etb.cohort
ORDER BY ca.cohort DESC;


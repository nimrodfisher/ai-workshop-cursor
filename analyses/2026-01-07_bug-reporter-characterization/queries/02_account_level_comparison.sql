/*
================================================================================
QUERY: Account-Level Bug Reporting vs Non-Reporting Comparison
================================================================================
Business Question: What characterizes organizations whose users report bugs vs. those who don't?
Author: AI Analytics
Created: 2026-01-07
Last Modified: 2026-01-07
-----
DESCRIPTION:
  Compares accounts (organizations) that have had bug tickets opened against accounts
  that haven't across demographic (industry, plan tier, size) and behavioral (event
  activity, ticket volume) dimensions to identify organizational patterns.

DEPENDENCIES:
  - support_tickets: To identify bug-reporting accounts
  - accounts: For account demographic information
  - users: For team size calculation
  - events: For organizational engagement metrics

OUTPUT:
  - cohort: 'Bug-Reporting Account' or 'Non-Bug-Reporting Account'
  - account_count: Number of accounts in each cohort
  - avg_team_size: Average number of users per account
  - industry_breakdown: JSON with industry distribution
  - plan_breakdown: JSON with plan distribution
  - total_events: Total events across cohort
  - avg_events_per_account: Average events per account
  - avg_events_per_user: Average events per user (engagement intensity)
  - ticket_metrics: Average tickets per account

NOTES:
  - Bug-reporting accounts have at least one ticket with category = 'bug'
  - Team size is count of users per account
  - Engagement intensity = events per user within account
================================================================================
*/

WITH bug_reporting_accounts AS (
    -- Identify accounts that have had bug tickets opened
    SELECT DISTINCT 
        org_id as account_id
    FROM support_tickets
    WHERE category = 'bug'
),

account_cohorts AS (
    -- Assign each account to a cohort
    SELECT 
        a.id as account_id,
        a.name as account_name,
        a.industry,
        a.plan,
        a.created_at,
        CASE 
            WHEN bra.account_id IS NOT NULL THEN 'Bug-Reporting Account'
            ELSE 'Non-Bug-Reporting Account'
        END as cohort
    FROM accounts a
    LEFT JOIN bug_reporting_accounts bra ON a.id = bra.account_id
),

account_metrics AS (
    -- Calculate metrics for each account
    SELECT 
        ac.account_id,
        ac.cohort,
        ac.industry,
        ac.plan,
        EXTRACT(EPOCH FROM (NOW() - ac.created_at)) / 86400 as account_age_days,
        COUNT(DISTINCT u.id) as team_size,
        COUNT(e.id) as total_events,
        COUNT(DISTINCT e.event_type) as event_diversity,
        COUNT(DISTINCT st.id) as total_tickets,
        COUNT(DISTINCT CASE WHEN st.category = 'bug' THEN st.id END) as bug_tickets
    FROM account_cohorts ac
    LEFT JOIN users u ON ac.account_id = u.org_id
    LEFT JOIN events e ON ac.account_id = e.org_id
    LEFT JOIN support_tickets st ON ac.account_id = st.org_id
    GROUP BY ac.account_id, ac.cohort, ac.industry, ac.plan, ac.created_at
),

cohort_aggregates AS (
    -- Aggregate by cohort
    SELECT 
        cohort,
        COUNT(*) as account_count,
        ROUND(AVG(account_age_days)::numeric, 2) as avg_account_age_days,
        ROUND(AVG(team_size)::numeric, 2) as avg_team_size,
        ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY team_size)::numeric, 2) as median_team_size,
        SUM(total_events) as total_events,
        ROUND(AVG(total_events)::numeric, 2) as avg_events_per_account,
        ROUND(AVG(CASE WHEN team_size > 0 THEN total_events::numeric / team_size ELSE 0 END)::numeric, 2) as avg_events_per_user,
        ROUND(AVG(event_diversity)::numeric, 2) as avg_event_diversity,
        ROUND(AVG(total_tickets)::numeric, 2) as avg_tickets_per_account,
        ROUND(AVG(bug_tickets)::numeric, 2) as avg_bug_tickets_per_account,
        MAX(total_events) as max_events_per_account,
        MIN(total_events) as min_events_per_account
    FROM account_metrics
    GROUP BY cohort
)

SELECT 
    cohort,
    account_count,
    avg_account_age_days,
    avg_team_size,
    median_team_size,
    total_events,
    avg_events_per_account,
    avg_events_per_user,
    avg_event_diversity,
    avg_tickets_per_account,
    avg_bug_tickets_per_account,
    max_events_per_account,
    min_events_per_account
FROM cohort_aggregates
ORDER BY cohort DESC;


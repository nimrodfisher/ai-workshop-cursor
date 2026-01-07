/*
================================================================================
QUERY: Behavioral Patterns - Event Activity Analysis
================================================================================
Business Question: Are bug reporters more or less active than other users?
Author: Nimrod Fisher
Created: 2026-01-07
Last Modified: 2026-01-07
-----
DESCRIPTION:
  Compares behavioral patterns between bug reporters and other users by analyzing:
  - Total event count per user
  - Event diversity (distinct event types)
  - Recent activity (last 30 days)
  - Activity span (time between first and last event)
  
  This identifies whether bug reporters are power users (high activity) or
  struggling users (low activity).

DEPENDENCIES:
  - public.support_tickets: To identify bug ticket reporters
  - public.events: User event/activity data

OUTPUT:
  - cohort: 'Bug Reporter' or 'Other User' (text)
  - user_count: Number of users analyzed (integer)
  - avg_total_events: Average events per user (numeric)
  - avg_distinct_event_types: Average event type diversity (numeric)
  - avg_events_last_30d: Average recent activity (numeric)
  - avg_activity_span_days: Average time between first/last event (numeric)

NOTES:
  - This is part of Phase 3: Main Analysis
  - Higher avg_total_events suggests power users
  - Lower activity may indicate user struggles or frustration
================================================================================
*/

WITH bug_ticket_users AS (
  SELECT DISTINCT opened_by AS user_id
  FROM support_tickets
  WHERE category = 'bug' AND opened_by IS NOT NULL
),
user_activity AS (
  SELECT 
    e.user_id,
    COUNT(*) AS total_events,
    COUNT(DISTINCT e.event_type) AS distinct_event_types,
    COUNT(CASE WHEN e.occurred_at >= NOW() - INTERVAL '30 days' THEN 1 END) AS events_last_30d,
    MIN(e.occurred_at) AS first_event,
    MAX(e.occurred_at) AS last_event
  FROM events e
  WHERE e.user_id IS NOT NULL
  GROUP BY e.user_id
)
SELECT 
  CASE WHEN btu.user_id IS NOT NULL THEN 'Bug Reporter' ELSE 'Other User' END AS cohort,
  COUNT(*) AS user_count,
  ROUND(AVG(ua.total_events), 2) AS avg_total_events,
  ROUND(AVG(ua.distinct_event_types), 2) AS avg_distinct_event_types,
  ROUND(AVG(ua.events_last_30d), 2) AS avg_events_last_30d,
  ROUND(AVG(DATE_PART('day', ua.last_event - ua.first_event)), 2) AS avg_activity_span_days
FROM user_activity ua
LEFT JOIN bug_ticket_users btu ON ua.user_id = btu.user_id
GROUP BY cohort
ORDER BY cohort;


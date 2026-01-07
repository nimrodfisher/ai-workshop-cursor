/*
================================================================================
QUERY: Event Type Distribution - EDA
================================================================================
Business Question: What are the most common event types in the system?
Author: Nimrod Fisher
Created: 2026-01-07
Last Modified: 2026-01-07
-----
DESCRIPTION:
  Analyzes the distribution of event types to understand user activities:
  - Count and percentage by event type
  - Unique users performing each event type
  - Recent activity (last 30 days)

DEPENDENCIES:
  - public.events: Event tracking data

OUTPUT:
  - event_type: Type of event (text)
  - total_events: Total event count (integer)
  - unique_users: Number of distinct users (integer)
  - events_last_30d: Recent event count (integer)
  - pct_of_total: Percentage of all events (numeric)

NOTES:
  - This is part of Phase 2: EDA
  - Helps understand what activities users are performing
================================================================================
*/

SELECT 
    event_type,
    COUNT(*) AS total_events,
    COUNT(DISTINCT user_id) AS unique_users,
    COUNT(CASE WHEN occurred_at >= NOW() - INTERVAL '30 days' THEN 1 END) AS events_last_30d,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM events), 2) AS pct_of_total
FROM events
WHERE event_type IS NOT NULL
GROUP BY event_type
ORDER BY total_events DESC;


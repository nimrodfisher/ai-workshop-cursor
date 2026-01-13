/*
================================================================================
QUERY: Specific Event Types - What Are Bug Reporters Doing?
================================================================================
Business Question: Which actions/events are most associated with bug reporters?
Author: Nimrod Fisher
Created: 2026-01-07
Last Modified: 2026-01-07
-----
DESCRIPTION:
  Identifies which specific event types are overrepresented among bug reporters
  compared to other users. For each event type, calculates:
  - Participation rate among bug reporters
  - Participation rate among other users
  - Overrepresentation ratio (how much more common among bug reporters)
  
  This reveals what activities bug reporters are performing before/after 
  encountering bugs.

DEPENDENCIES:
  - public.support_tickets: To identify bug ticket reporters
  - public.events: Event tracking data
  - public.users: User count for percentage calculations

OUTPUT:
  - event_type: Type of event (text)
  - bug_reporter_users: Count of bug reporters who performed this event (integer)
  - other_users: Count of other users who performed this event (integer)
  - pct_bug_reporters: % of bug reporters who did this (numeric)
  - pct_other_users: % of other users who did this (numeric)
  - overrepresentation_ratio: Ratio showing association strength (numeric)

NOTES:
  - This is part of Phase 3: Main Analysis
  - Ratio > 1.0 means bug reporters do this more than others
  - Ratio < 1.0 means bug reporters do this less than others
  - High ratio events reveal bug reporter behavioral signatures
================================================================================
*/

WITH bug_ticket_users AS (
  SELECT DISTINCT opened_by AS user_id
  FROM support_tickets
  WHERE category = 'bug' AND opened_by IS NOT NULL
),
event_participation AS (
  SELECT 
    e.event_type,
    COUNT(DISTINCT CASE WHEN btu.user_id IS NOT NULL THEN e.user_id END) AS bug_reporter_users,
    COUNT(DISTINCT CASE WHEN btu.user_id IS NULL THEN e.user_id END) AS other_users
  FROM events e
  LEFT JOIN bug_ticket_users btu ON e.user_id = btu.user_id
  WHERE e.user_id IS NOT NULL
  GROUP BY e.event_type
)
SELECT 
  event_type,
  bug_reporter_users,
  other_users,
  ROUND(100.0 * bug_reporter_users / (SELECT COUNT(DISTINCT user_id) FROM bug_ticket_users), 2) AS pct_bug_reporters,
  ROUND(100.0 * other_users / (SELECT COUNT(*) FROM users WHERE id NOT IN (SELECT user_id FROM bug_ticket_users)), 2) AS pct_other_users,
  ROUND(bug_reporter_users::numeric / NULLIF(other_users, 0), 2) AS overrepresentation_ratio
FROM event_participation
ORDER BY overrepresentation_ratio DESC;





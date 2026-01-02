/*
================================================================================
QUERY: Engagement Levels of Bug Reporters vs. Others
================================================================================
Business Question: Are bug reporters more engaged with the product than non-reporters?
Author: AI Analysis Assistant
Created: 2026-01-01
Last Modified: 2026-01-01
-----
DESCRIPTION:
  Compares the average event activity (engagement) of users who have reported 
  at least one bug vs. those who haven't. This helps determine if bugs are 
  being discovered by "power users" who use the product more intensively.

DEPENDENCIES:
  - users: Base user list
  - support_tickets: To identify bug reporters
  - events: To calculate engagement/activity level

OUTPUT:
  - user_type: Categorized as 'Bug Reporter' or 'Non-Reporter'
  - user_count: Count of users in each category
  - avg_events_per_user: Average number of events triggered by these users

NOTES:
  - Uses a CTE to identify unique bug reporters.
  - Left joins events to include users with no activity.
================================================================================
*/

WITH bug_reporters AS (
    SELECT DISTINCT opened_by FROM support_tickets WHERE category = 'bug'
),
user_activity AS (
    SELECT 
        u.id,
        CASE WHEN br.opened_by IS NOT NULL THEN 'Bug Reporter' ELSE 'Non-Reporter' END as user_type,
        COUNT(e.id) as event_count
    FROM users u
    LEFT JOIN bug_reporters br ON u.id = br.opened_by
    LEFT JOIN events e ON u.id = e.user_id
    GROUP BY u.id, br.opened_by
)
SELECT 
    user_type,
    COUNT(*) as user_count,
    ROUND(AVG(event_count), 2) as avg_events_per_user
FROM user_activity
GROUP BY user_type;


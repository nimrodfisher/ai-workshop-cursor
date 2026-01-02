/*
================================================================================
QUERY: Bug Tickets by User Role
================================================================================
Business Question: What user roles are most likely to report bugs?
Author: AI Analysis Assistant
Created: 2026-01-01
Last Modified: 2026-01-01
-----
DESCRIPTION:
  Analyzes bug reporting frequency based on the role of the user who opened 
  the ticket. Helps distinguish between administrative/technical bugs vs. 
  general usage bugs.

DEPENDENCIES:
  - users: To get user roles
  - support_tickets: To link tickets to reporters

OUTPUT:
  - role: The role of the reporting user (admin, analyst, viewer)
  - bug_ticket_count: Total bugs reported by this role
  - user_count: Total number of users with this role in the system
  - bugs_per_user: Normalized reporting frequency per user

NOTES:
  - Higher frequency among admins often suggests setup or system-wide issues.
================================================================================
*/

SELECT 
    u.role,
    COUNT(st.id) as bug_ticket_count,
    COUNT(DISTINCT u.id) as user_count,
    ROUND(COUNT(st.id)::numeric / NULLIF(COUNT(DISTINCT u.id), 0), 2) as bugs_per_user
FROM users u
LEFT JOIN support_tickets st ON u.id = st.opened_by AND st.category = 'bug'
GROUP BY u.role
ORDER BY bug_ticket_count DESC;


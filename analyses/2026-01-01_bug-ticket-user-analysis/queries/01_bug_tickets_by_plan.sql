/*
================================================================================
QUERY: Bug Tickets by Account Plan Tier
================================================================================
Business Question: Which account segments (plan tier) open the most bug-related tickets?
Author: AI Analysis Assistant
Created: 2026-01-01
Last Modified: 2026-01-01
-----
DESCRIPTION:
  This query calculates the number of bug tickets per account plan tier (Free, 
  Pro, Enterprise). It also calculates a density metric (bugs per account) to 
  normalize for the varying number of accounts in each tier.

DEPENDENCIES:
  - accounts: To get plan tier for each organization
  - support_tickets: To filter for 'bug' category tickets

OUTPUT:
  - plan: The subscription plan tier
  - bug_ticket_count: Total number of bug tickets for this tier
  - account_count: Number of unique accounts in this tier
  - bugs_per_account: Average bug tickets per account in this tier

NOTES:
  - Uses a LEFT JOIN to ensure all plan tiers are represented, even if 0 bugs.
  - Category is filtered specifically for 'bug'.
================================================================================
*/

SELECT 
    a.plan,
    COUNT(st.id) as bug_ticket_count,
    COUNT(DISTINCT a.id) as account_count,
    ROUND(COUNT(st.id)::numeric / NULLIF(COUNT(DISTINCT a.id), 0), 2) as bugs_per_account
FROM accounts a
LEFT JOIN support_tickets st ON a.id = st.org_id AND st.category = 'bug'
GROUP BY a.plan
ORDER BY bug_ticket_count DESC;


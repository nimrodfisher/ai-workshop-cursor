/*
================================================================================
QUERY: Bug Tickets by Industry
================================================================================
Business Question: Which industries open the most bug-related tickets?
Author: AI Analysis Assistant
Created: 2026-01-01
Last Modified: 2026-01-01
-----
DESCRIPTION:
  This query breaks down bug tickets by the industry of the reporting account.
  It helps identify if certain verticals are encountering more issues or are 
  more vocal about bugs.

DEPENDENCIES:
  - accounts: To get industry classification
  - support_tickets: To filter for 'bug' category tickets

OUTPUT:
  - industry: The industry category of the account
  - bug_ticket_count: Total bug tickets reported by this industry
  - account_count: Number of unique accounts in this industry
  - bugs_per_account: Density metric for bug reporting

NOTES:
  - Industry categories include MarTech, eCommerce, EdTech, etc.
================================================================================
*/

SELECT 
    a.industry,
    COUNT(st.id) as bug_ticket_count,
    COUNT(DISTINCT a.id) as account_count,
    ROUND(COUNT(st.id)::numeric / NULLIF(COUNT(DISTINCT a.id), 0), 2) as bugs_per_account
FROM accounts a
LEFT JOIN support_tickets st ON a.id = st.org_id AND st.category = 'bug'
GROUP BY a.industry
ORDER BY bug_ticket_count DESC;


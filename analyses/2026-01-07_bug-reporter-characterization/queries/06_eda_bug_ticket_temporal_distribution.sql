/*
================================================================================
QUERY: Bug Ticket Temporal Distribution - EDA
================================================================================
Business Question: When are bug tickets being opened? Are there temporal patterns?
Author: Nimrod Fisher
Created: 2026-01-07
Last Modified: 2026-01-07
-----
DESCRIPTION:
  Analyzes temporal patterns in bug ticket creation to identify:
  - Monthly distribution of bug tickets
  - Day of week patterns
  - Open vs closed status over time

DEPENDENCIES:
  - public.support_tickets: Source table for bug ticket analysis

OUTPUT:
  - month: Month when tickets were opened (date)
  - total_bug_tickets: Count of bug tickets opened (integer)
  - open_tickets: Count still open (integer)
  - closed_tickets: Count that have been closed (integer)
  - pct_closed: Percentage closed (numeric)

NOTES:
  - This is part of Phase 2: EDA
  - Helps understand if bug reporting is increasing/decreasing over time
================================================================================
*/

SELECT 
    DATE_TRUNC('month', opened_at)::date AS month,
    COUNT(*) AS total_bug_tickets,
    COUNT(CASE WHEN status = 'open' AND closed_at IS NULL THEN 1 END) AS open_tickets,
    COUNT(CASE WHEN status = 'closed' OR closed_at IS NOT NULL THEN 1 END) AS closed_tickets,
    ROUND(100.0 * COUNT(CASE WHEN status = 'closed' OR closed_at IS NOT NULL THEN 1 END) / COUNT(*), 2) AS pct_closed
FROM support_tickets
WHERE category = 'bug'
GROUP BY DATE_TRUNC('month', opened_at)
ORDER BY month DESC;


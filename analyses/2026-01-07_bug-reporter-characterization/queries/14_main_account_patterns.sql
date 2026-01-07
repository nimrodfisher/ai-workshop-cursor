/*
================================================================================
QUERY: Account-Level Patterns - Multi-Ticket Accounts
================================================================================
Business Question: Are bug tickets concentrated in specific accounts, and what 
                  characterizes those accounts?
Author: Nimrod Fisher
Created: 2026-01-07
Last Modified: 2026-01-07
-----
DESCRIPTION:
  Analyzes account-level patterns to determine if bug reporting is:
  - Concentrated in a few problem accounts, or
  - Widespread across many accounts
  
  Segments accounts into three groups:
  - Multi-Bug Accounts (2+ bug tickets)
  - Single-Bug Accounts (exactly 1 bug ticket)
  - No Bug Tickets (0 bug tickets)
  
  Compares these groups across dimensions like team size, event activity,
  and non-bug support ticket volume.

DEPENDENCIES:
  - public.support_tickets: Bug ticket counts per account
  - public.accounts: Account information
  - public.users: Team size per account
  - public.subscriptions: Subscription counts
  - public.events: Activity levels

OUTPUT:
  - account_group: Multi/Single/No Bug Tickets (text)
  - account_count: Number of accounts in this group (integer)
  - avg_users: Average team size (numeric)
  - avg_events: Average event activity (numeric)
  - avg_non_bug_tickets: Average other support tickets (numeric)
  - plans_represented: Which plan tiers are in this group (text)

NOTES:
  - This is part of Phase 3: Main Analysis
  - Multi-Bug Accounts may indicate systemic product issues
  - Comparing avg_events reveals if active users encounter more bugs
================================================================================
*/

WITH account_bug_tickets AS (
  SELECT 
    org_id,
    COUNT(*) AS bug_ticket_count,
    MIN(opened_at) AS first_bug_ticket,
    MAX(opened_at) AS latest_bug_ticket
  FROM support_tickets
  WHERE category = 'bug'
  GROUP BY org_id
),
account_metrics AS (
  SELECT 
    a.id AS org_id,
    a.name,
    a.plan,
    a.industry,
    COUNT(DISTINCT u.id) AS user_count,
    COUNT(DISTINCT s.id) AS subscription_count,
    COUNT(DISTINCT e.id) AS total_events,
    COUNT(DISTINCT st.id) AS total_tickets,
    COUNT(DISTINCT CASE WHEN st.category != 'bug' THEN st.id END) AS non_bug_tickets
  FROM accounts a
  LEFT JOIN users u ON a.id = u.org_id
  LEFT JOIN subscriptions s ON a.id = s.org_id
  LEFT JOIN events e ON a.id = e.org_id
  LEFT JOIN support_tickets st ON a.id = st.org_id
  GROUP BY a.id, a.name, a.plan, a.industry
)
SELECT 
  CASE 
    WHEN abt.bug_ticket_count >= 2 THEN 'Multi-Bug Accounts'
    WHEN abt.bug_ticket_count = 1 THEN 'Single-Bug Accounts'
    ELSE 'No Bug Tickets'
  END AS account_group,
  COUNT(*) AS account_count,
  ROUND(AVG(am.user_count), 2) AS avg_users,
  ROUND(AVG(am.total_events), 2) AS avg_events,
  ROUND(AVG(am.non_bug_tickets), 2) AS avg_non_bug_tickets,
  STRING_AGG(DISTINCT am.plan, ', ') AS plans_represented
FROM account_metrics am
LEFT JOIN account_bug_tickets abt ON am.org_id = abt.org_id
GROUP BY account_group
ORDER BY 
  CASE account_group
    WHEN 'Multi-Bug Accounts' THEN 1
    WHEN 'Single-Bug Accounts' THEN 2
    ELSE 3
  END;


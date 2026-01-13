/*
================================================================================
QUERY: Bug Reporter Demographics vs All Users
================================================================================
Business Question: How do bug ticket users differ demographically from other users?
Author: Nimrod Fisher
Created: 2026-01-07
Last Modified: 2026-01-07
-----
DESCRIPTION:
  Compares demographic characteristics of users who opened bug tickets against
  all other users in the system. Analyzes differences in:
  - User role distribution (admin/analyst/viewer)
  - Account plan tier (enterprise/pro/free)
  - Account industry vertical
  - User and account tenure (age in days)

DEPENDENCIES:
  - public.support_tickets: To identify bug ticket reporters
  - public.users: User demographics and roles
  - public.accounts: Account plan and industry information

OUTPUT:
  - cohort: 'Bug Reporter' or 'Other User' (text)
  - role: User role (text)
  - plan: Account plan tier (text)
  - industry: Account industry (text)
  - user_count: Number of users in this segment (integer)
  - avg_user_tenure_days: Average user age in days (numeric)
  - avg_account_tenure_days: Average account age in days (numeric)

NOTES:
  - This is part of Phase 3: Main Analysis
  - Results will reveal if bug reporters have distinct demographic profiles
  - GROUP BY cohort, role, plan, industry creates granular segments
================================================================================
*/

WITH bug_ticket_users AS (
  SELECT DISTINCT opened_by AS user_id
  FROM support_tickets
  WHERE category = 'bug' AND opened_by IS NOT NULL
),
user_cohorts AS (
  SELECT 
    u.id,
    u.role,
    u.created_at AS user_created_at,
    a.plan,
    a.industry,
    a.created_at AS account_created_at,
    CASE WHEN btu.user_id IS NOT NULL THEN 'Bug Reporter' ELSE 'Other User' END AS cohort
  FROM users u
  JOIN accounts a ON u.org_id = a.id
  LEFT JOIN bug_ticket_users btu ON u.id = btu.user_id
)
SELECT 
  cohort,
  role,
  plan,
  industry,
  COUNT(*) AS user_count,
  ROUND(AVG(DATE_PART('day', NOW() - user_created_at)), 2) AS avg_user_tenure_days,
  ROUND(AVG(DATE_PART('day', NOW() - account_created_at)), 2) AS avg_account_tenure_days
FROM user_cohorts
GROUP BY cohort, role, plan, industry
ORDER BY cohort, user_count DESC;





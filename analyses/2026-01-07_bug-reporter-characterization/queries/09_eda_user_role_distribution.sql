/*
================================================================================
QUERY: User Role Distribution - EDA
================================================================================
Business Question: What is the distribution of user roles in the system?
Author: Nimrod Fisher
Created: 2026-01-07
Last Modified: 2026-01-07
-----
DESCRIPTION:
  Analyzes the distribution of users by role:
  - Count and percentage by role (admin/analyst/viewer)
  - Average account plan tier by role
  - Average user tenure by role

DEPENDENCIES:
  - public.users: User role information
  - public.accounts: Account plan information

OUTPUT:
  - role: User role (text)
  - user_count: Number of users (integer)
  - pct_of_total: Percentage of all users (numeric)
  - avg_user_age_days: Average user tenure in days (numeric)

NOTES:
  - This is part of Phase 2: EDA
  - Establishes baseline to compare bug reporters against
================================================================================
*/

SELECT 
    u.role,
    COUNT(*) AS user_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM users), 2) AS pct_of_total,
    ROUND(AVG(DATE_PART('day', NOW() - u.created_at)), 0) AS avg_user_age_days,
    STRING_AGG(DISTINCT a.plan, ', ' ORDER BY a.plan) AS plans_represented
FROM users u
JOIN accounts a ON u.org_id = a.id
GROUP BY u.role
ORDER BY user_count DESC;





/*
================================================================================
QUERY: Account Plan Distribution - EDA
================================================================================
Business Question: What is the distribution of accounts across plan tiers?
Author: Nimrod Fisher
Created: 2026-01-07
Last Modified: 2026-01-07
-----
DESCRIPTION:
  Analyzes the distribution of accounts by plan tier to establish baseline:
  - Count and percentage by plan (Free/Pro/Enterprise)
  - Average users per account by plan
  - Average subscription revenue by plan

DEPENDENCIES:
  - public.accounts: Account plan information
  - public.users: User count per account
  - public.subscriptions: Revenue information

OUTPUT:
  - plan: Plan tier name (text)
  - account_count: Number of accounts (integer)
  - pct_of_total: Percentage of all accounts (numeric)
  - avg_users_per_account: Average user count (numeric)
  - avg_active_subs: Average active subscriptions (numeric)

NOTES:
  - This is part of Phase 2: EDA
  - Establishes baseline to compare bug ticket accounts against
================================================================================
*/

SELECT 
    a.plan,
    COUNT(DISTINCT a.id) AS account_count,
    ROUND(100.0 * COUNT(DISTINCT a.id) / (SELECT COUNT(*) FROM accounts), 2) AS pct_of_total,
    ROUND(AVG(user_counts.user_count), 2) AS avg_users_per_account,
    ROUND(AVG(sub_counts.active_subs), 2) AS avg_active_subs
FROM accounts a
LEFT JOIN (
    SELECT org_id, COUNT(*) AS user_count
    FROM users
    GROUP BY org_id
) user_counts ON a.id = user_counts.org_id
LEFT JOIN (
    SELECT org_id, COUNT(*) AS active_subs
    FROM subscriptions
    WHERE status = 'active'
    GROUP BY org_id
) sub_counts ON a.id = sub_counts.org_id
GROUP BY a.plan
ORDER BY account_count DESC;


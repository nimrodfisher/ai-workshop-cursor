/*
================================================================================
QUERY: Industry Distribution - EDA
================================================================================
Business Question: How are accounts distributed across industries?
Author: Nimrod Fisher
Created: 2026-01-07
Last Modified: 2026-01-07
-----
DESCRIPTION:
  Analyzes the distribution of accounts by industry vertical:
  - Count and percentage by industry
  - Average account age by industry
  - Average users per industry

DEPENDENCIES:
  - public.accounts: Industry and account information
  - public.users: User count per account

OUTPUT:
  - industry: Industry name (text)
  - account_count: Number of accounts (integer)
  - pct_of_total: Percentage of all accounts (numeric)
  - avg_users_per_account: Average user count (numeric)
  - avg_account_age_days: Average account age in days (numeric)

NOTES:
  - This is part of Phase 2: EDA
  - Helps identify if certain industries report more bugs
================================================================================
*/

SELECT 
    a.industry,
    COUNT(DISTINCT a.id) AS account_count,
    ROUND(100.0 * COUNT(DISTINCT a.id) / (SELECT COUNT(*) FROM accounts), 2) AS pct_of_total,
    ROUND(AVG(user_counts.user_count), 2) AS avg_users_per_account,
    ROUND(AVG(DATE_PART('day', NOW() - a.created_at)), 0) AS avg_account_age_days
FROM accounts a
LEFT JOIN (
    SELECT org_id, COUNT(*) AS user_count
    FROM users
    GROUP BY org_id
) user_counts ON a.id = user_counts.org_id
GROUP BY a.industry
ORDER BY account_count DESC;





/*
================================================================================
QUERY: Subscription & Revenue Patterns
================================================================================
Business Question: Do bug reporters have different subscription/payment patterns?
Author: Nimrod Fisher
Created: 2026-01-07
Last Modified: 2026-01-07
-----
DESCRIPTION:
  Compares subscription and revenue metrics between accounts with bug tickets
  and accounts without bug tickets. Analyzes:
  - Active vs canceled subscription rates
  - Average monthly price (ARPU)
  - Subscription tenure/longevity
  - Churn indicators
  
  This reveals whether bug reporting is associated with:
  - Higher-value customers (who use product more)
  - At-risk customers (who may churn)
  - No correlation with revenue

DEPENDENCIES:
  - public.support_tickets: To identify bug ticket accounts
  - public.subscriptions: Subscription status and pricing

OUTPUT:
  - cohort: 'Bug Ticket Accounts' or 'Other Accounts' (text)
  - account_count: Number of accounts (integer)
  - avg_subs_per_account: Average subscription count (numeric)
  - avg_active_subs: Average active subscriptions (numeric)
  - avg_canceled_subs: Average canceled subscriptions (numeric)
  - avg_monthly_price: Average subscription price (numeric)
  - avg_account_mrr: Average total MRR per account (numeric)
  - avg_subscription_tenure_days: Average subscription age (numeric)

NOTES:
  - This is part of Phase 3: Main Analysis
  - Higher avg_canceled_subs may indicate churn risk
  - Higher avg_monthly_price suggests valuable customer segment
  - Lower tenure may indicate new accounts still onboarding
================================================================================
*/

WITH bug_ticket_accounts AS (
  SELECT DISTINCT org_id
  FROM support_tickets
  WHERE category = 'bug'
),
subscription_metrics AS (
  SELECT 
    s.org_id,
    COUNT(*) AS subscription_count,
    COUNT(CASE WHEN s.status = 'active' THEN 1 END) AS active_subs,
    COUNT(CASE WHEN s.canceled_at IS NOT NULL THEN 1 END) AS canceled_subs,
    AVG(s.monthly_price) AS avg_monthly_price,
    SUM(CASE WHEN s.status = 'active' THEN s.monthly_price ELSE 0 END) AS total_mrr,
    AVG(DATE_PART('day', COALESCE(s.canceled_at::timestamp, CURRENT_TIMESTAMP) - s.started_at::timestamp)) AS avg_sub_tenure_days
  FROM subscriptions s
  GROUP BY s.org_id
)
SELECT 
  CASE WHEN bta.org_id IS NOT NULL THEN 'Bug Ticket Accounts' ELSE 'Other Accounts' END AS cohort,
  COUNT(*) AS account_count,
  ROUND(AVG(sm.subscription_count), 2) AS avg_subs_per_account,
  ROUND(AVG(sm.active_subs), 2) AS avg_active_subs,
  ROUND(AVG(sm.canceled_subs), 2) AS avg_canceled_subs,
  ROUND(AVG(sm.avg_monthly_price), 2) AS avg_monthly_price,
  ROUND(AVG(sm.total_mrr), 2) AS avg_account_mrr,
  ROUND(AVG(sm.avg_sub_tenure_days), 2) AS avg_subscription_tenure_days
FROM subscription_metrics sm
LEFT JOIN bug_ticket_accounts bta ON sm.org_id = bta.org_id
GROUP BY cohort
ORDER BY cohort;





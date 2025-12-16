/*
================================================================================
QUERY: MRR by Plan - Last 12 Months
================================================================================
Business Question: How has MRR changed by plan over the last 12 months?
Author: AI Analytics Hub
Created: 2024-12-15
Last Modified: 2024-12-15
-----
DESCRIPTION:
 This query calculates Monthly Recurring Revenue (MRR) by subscription plan
 for each of the last 12 months. It identifies active subscriptions for each
 month and aggregates revenue by plan, including month-over-month change
 calculations.

DEPENDENCIES:
 - public.subscriptions: Contains subscription records with monthly_price,
   started_at, canceled_at, and org_id
 - public.accounts: Contains account information with plan assignments

OUTPUT:
 - month: Month in YYYY-MM-01 format
 - plan: Subscription plan name (free, pro, enterprise, or Unknown)
 - mrr: Total MRR for the plan in that month (rounded to 2 decimals)
 - subscription_count: Number of active subscriptions for the plan
 - org_count: Number of unique organizations with active subscriptions
 - previous_month_mrr: MRR from the previous month (for comparison)
 - mrr_change_percent: Month-over-month percentage change in MRR

NOTES:
 - A subscription is considered active in a month if:
   * started_at <= last day of the month
   * AND (canceled_at IS NULL OR canceled_at > last day of the month)
 - Only subscriptions with monthly_price > 0 are included
 - Accounts without a plan assignment are labeled as 'Unknown'
 - Month-over-month change is calculated using LAG window function
================================================================================
*/

WITH month_series AS (
    -- Generate last 12 months from current date
    SELECT 
        DATE_TRUNC('month', month_date) AS month
    FROM generate_series(
        DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '11 months',
        DATE_TRUNC('month', CURRENT_DATE),
        '1 month'::interval
    ) AS month_date
),

active_subscriptions_by_month AS (
    -- For each month, identify which subscriptions were active
    SELECT 
        ms.month,
        s.id AS subscription_id,
        s.org_id,
        s.monthly_price,
        s.started_at,
        s.canceled_at
    FROM month_series ms
    CROSS JOIN subscriptions s
    WHERE s.started_at IS NOT NULL
      AND s.monthly_price IS NOT NULL
      AND s.monthly_price > 0
      -- Subscription was active if it started before or during this month
      AND s.started_at <= (ms.month + INTERVAL '1 month' - INTERVAL '1 day')
      -- And either not canceled, or canceled after this month
      AND (s.canceled_at IS NULL OR s.canceled_at > (ms.month + INTERVAL '1 month' - INTERVAL '1 day'))
),

mrr_by_month_and_plan AS (
    -- Calculate MRR by month and plan
    SELECT 
        asm.month,
        COALESCE(a.plan, 'Unknown') AS plan,
        SUM(asm.monthly_price) AS mrr,
        COUNT(DISTINCT asm.subscription_id) AS subscription_count,
        COUNT(DISTINCT asm.org_id) AS org_count
    FROM active_subscriptions_by_month asm
    LEFT JOIN accounts a ON asm.org_id = a.id
    GROUP BY asm.month, COALESCE(a.plan, 'Unknown')
)

-- Final output: MRR by plan over time with month-over-month change
SELECT 
    month,
    plan,
    ROUND(mrr::numeric, 2) AS mrr,
    subscription_count,
    org_count,
    -- Calculate month-over-month change
    LAG(mrr) OVER (PARTITION BY plan ORDER BY month) AS previous_month_mrr,
    ROUND(
        ((mrr - LAG(mrr) OVER (PARTITION BY plan ORDER BY month)) / 
         NULLIF(LAG(mrr) OVER (PARTITION BY plan ORDER BY month), 0) * 100)::numeric, 
        2
    ) AS mrr_change_percent
FROM mrr_by_month_and_plan
ORDER BY month DESC, mrr DESC;

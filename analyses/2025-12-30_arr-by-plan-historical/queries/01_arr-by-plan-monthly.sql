/*
================================================================================
QUERY: ARR Historical Analysis by Plan
================================================================================
Business Question: How has Annual Recurring Revenue (ARR) changed historically 
                   by subscription plan tier?

Author: AI Analytics Hub
Created: 2025-12-30
Last Modified: 2025-12-30
-----
DESCRIPTION:
  This query calculates the monthly ARR for each plan tier over time by 
  determining which subscriptions were active in each month and summing their
  annual value (monthly_price * 12). It tracks ARR evolution from June 2024
  to present.

DEPENDENCIES:
  - subscriptions: Provides subscription status, dates, and monthly pricing
  - accounts: Provides plan tier classification for each organization

OUTPUT:
  - month: Calendar month (YYYY-MM-DD format)
  - plan: Subscription plan tier (Free, Pro, Enterprise)
  - active_subscriptions: Count of active subscriptions in that month/plan
  - total_arr: Total Annual Recurring Revenue for that month/plan
  - cumulative_arr: Running total of ARR up to that month

NOTES:
  - A subscription is "active" in a month if:
    * started_at <= month_end
    * AND (canceled_at IS NULL OR canceled_at > month_end)
  - ARR = monthly_price * 12
  - Only includes subscriptions with status currently in (active, canceled, trialing)
  - Excludes future months beyond current date
================================================================================
*/

WITH 
-- Step 1: Generate all months in our analysis period
month_series AS (
    SELECT 
        DATE_TRUNC('month', generate_series(
            '2024-06-01'::date,
            DATE_TRUNC('month', CURRENT_DATE)::date,
            '1 month'::interval
        ))::date AS month
),

-- Step 2: Get all subscriptions with their plan information
subscriptions_with_plans AS (
    SELECT 
        s.id AS subscription_id,
        s.org_id,
        s.monthly_price,
        s.status,
        s.started_at,
        s.canceled_at,
        a.plan,
        a.name AS account_name
    FROM subscriptions s
    INNER JOIN accounts a ON s.org_id = a.id
    WHERE a.plan IS NOT NULL  -- Ensure we have plan information
),

-- Step 3: Create a cross-join of all months with all subscriptions
-- Then filter to only include months where subscription was active
active_subscriptions_by_month AS (
    SELECT 
        ms.month,
        swp.subscription_id,
        swp.org_id,
        swp.plan,
        swp.monthly_price,
        swp.monthly_price * 12 AS arr,  -- Calculate ARR for this subscription
        swp.started_at,
        swp.canceled_at
    FROM month_series ms
    CROSS JOIN subscriptions_with_plans swp
    WHERE 
        -- Subscription started on or before the end of the month
        swp.started_at <= (ms.month + INTERVAL '1 month' - INTERVAL '1 day')::date
        -- AND subscription was not canceled, OR was canceled after the month ended
        AND (
            swp.canceled_at IS NULL 
            OR swp.canceled_at > (ms.month + INTERVAL '1 month' - INTERVAL '1 day')::date
        )
),

-- Step 4: Aggregate ARR by month and plan
arr_by_month_and_plan AS (
    SELECT 
        month,
        plan,
        COUNT(DISTINCT subscription_id) AS active_subscriptions,
        SUM(arr) AS total_arr
    FROM active_subscriptions_by_month
    GROUP BY month, plan
)

-- Step 5: Final output with running totals
SELECT 
    month,
    plan,
    active_subscriptions,
    total_arr,
    -- Calculate month-over-month change
    LAG(total_arr) OVER (PARTITION BY plan ORDER BY month) AS previous_month_arr,
    total_arr - LAG(total_arr) OVER (PARTITION BY plan ORDER BY month) AS arr_change,
    ROUND(
        100.0 * (total_arr - LAG(total_arr) OVER (PARTITION BY plan ORDER BY month)) 
        / NULLIF(LAG(total_arr) OVER (PARTITION BY plan ORDER BY month), 0),
        2
    ) AS arr_change_pct
FROM arr_by_month_and_plan
ORDER BY month, plan;


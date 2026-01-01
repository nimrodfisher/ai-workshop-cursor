/*
================================================================================
QUERY: ARR Historical Trends by Plan
================================================================================
Business Question: How has our Annual Recurring Revenue (ARR) changed over time,
broken down by subscription plan tier?

Author: AI Analysis Assistant
Created: 2025-12-30
Last Modified: 2025-12-30
-----
DESCRIPTION:
  This query calculates ARR (monthly_price * 12) for each subscription plan
  over time, showing how revenue composition has evolved. It creates a monthly
  time series from the earliest subscription start date to present, calculating
  active ARR at each point in time.

DEPENDENCIES:
  - subscriptions: Subscription records with pricing, status, start and end dates
  - accounts: Account information including plan tier classification

OUTPUT:
  - month: First day of each month (date)
  - plan: Subscription plan tier (text)
  - active_subscriptions: Count of active subscriptions in that month (integer)
  - arr: Annual Recurring Revenue for that plan in that month (numeric)

NOTES:
  - A subscription is considered active in a month if:
    * started_at <= end of month
    * (canceled_at IS NULL OR canceled_at >= start of month)
  - ARR is calculated as: monthly_price * 12
  - Excludes subscriptions with NULL monthly_price
  - Groups by both month and plan to show revenue composition over time
================================================================================
*/

-- Section: Generate monthly time series
-- Purpose: Create a series of months from earliest subscription to present
-- Logic: Use generate_series to create first day of each month
WITH date_series AS (
    SELECT 
        DATE_TRUNC('month', MIN(started_at))::date AS min_month,
        DATE_TRUNC('month', CURRENT_DATE)::date AS max_month
    FROM subscriptions
),

months AS (
    SELECT 
        generate_series(
            (SELECT min_month FROM date_series),
            (SELECT max_month FROM date_series),
            INTERVAL '1 month'
        )::date AS month
),

-- Section: Calculate active subscriptions per month per plan
-- Purpose: Determine which subscriptions were active in each month
-- Logic: Join subscriptions to months where subscription was active during that month
-- Active means: started before/during month AND (not canceled OR canceled after month started)
active_subs AS (
    SELECT 
        m.month,
        a.plan,
        s.id AS subscription_id,
        s.monthly_price,
        s.started_at,
        s.canceled_at,
        s.status
    FROM months m
    CROSS JOIN subscriptions s
    JOIN accounts a ON s.org_id = a.id
    WHERE 
        -- Subscription started before or during this month
        s.started_at <= (m.month + INTERVAL '1 month' - INTERVAL '1 day')::date
        -- AND subscription was still active at start of this month
        AND (
            s.canceled_at IS NULL 
            OR s.canceled_at >= m.month
        )
        -- Exclude subscriptions with missing price
        AND s.monthly_price IS NOT NULL
),

-- Section: Aggregate ARR by month and plan
-- Purpose: Calculate total ARR and subscription count for each plan in each month
-- Logic: Sum monthly_price * 12 and count subscriptions, grouped by month and plan
arr_by_plan AS (
    SELECT 
        month,
        plan,
        COUNT(DISTINCT subscription_id) AS active_subscriptions,
        -- ARR = Sum of (monthly price * 12) for all active subscriptions
        SUM(monthly_price * 12) AS arr
    FROM active_subs
    GROUP BY month, plan
)

-- Final output: Monthly ARR trends by plan
SELECT 
    month,
    plan,
    active_subscriptions,
    ROUND(arr, 2) AS arr
FROM arr_by_plan
ORDER BY month ASC, plan ASC;



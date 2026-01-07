/*
================================================================================
QUERY: High-Value Customer Bug Reporting Analysis
================================================================================
Business Question: Are high-value customers (by MRR) more or less likely to report bugs?
Author: AI Analytics
Created: 2026-01-07
Last Modified: 2026-01-07
-----
DESCRIPTION:
  Analyzes bug reporting rates across different customer value segments based on
  Monthly Recurring Revenue (MRR). Segments accounts by MRR quartiles and compares
  bug reporting prevalence, frequency, and patterns.

DEPENDENCIES:
  - subscriptions: For MRR calculation (active subscriptions only)
  - accounts: For account information
  - support_tickets: For bug ticket data

OUTPUT:
  - mrr_segment: Revenue quartile (High/Medium/Low/No Subscription)
  - account_count: Number of accounts in segment
  - avg_mrr: Average MRR for segment
  - accounts_with_bugs: Number of accounts that reported bugs
  - bug_reporting_rate: Percentage of accounts reporting bugs
  - total_bug_tickets: Total bug tickets from segment
  - avg_bug_tickets_per_account: Average bug tickets across all accounts
  - avg_bug_tickets_per_reporting_account: Average among those who reported

NOTES:
  - MRR calculated from active subscriptions only
  - Quartiles: High (top 25%), Medium (25-75%), Low (bottom 25%)
  - No Subscription accounts handled separately
  - Revenue segments help identify if customer value correlates with bug reporting
================================================================================
*/

WITH account_mrr AS (
    -- Calculate MRR for each account
    SELECT 
        a.id as account_id,
        a.name as account_name,
        a.plan,
        a.industry,
        COALESCE(SUM(s.monthly_price), 0) as total_mrr
    FROM accounts a
    LEFT JOIN subscriptions s ON a.id = s.org_id AND s.status = 'active'
    GROUP BY a.id, a.name, a.plan, a.industry
),

mrr_quartiles AS (
    -- Calculate quartile breakpoints
    SELECT 
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY total_mrr) as q1,
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY total_mrr) as q2,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY total_mrr) as q3
    FROM account_mrr
    WHERE total_mrr > 0
),

account_segments AS (
    -- Assign each account to an MRR segment
    SELECT 
        am.account_id,
        am.account_name,
        am.plan,
        am.industry,
        am.total_mrr,
        CASE 
            WHEN am.total_mrr = 0 THEN 'No Subscription'
            WHEN am.total_mrr <= mq.q1 THEN 'Low MRR'
            WHEN am.total_mrr <= mq.q3 THEN 'Medium MRR'
            ELSE 'High MRR'
        END as mrr_segment
    FROM account_mrr am
    CROSS JOIN mrr_quartiles mq
),

bug_ticket_counts AS (
    -- Count bug tickets per account
    SELECT 
        org_id as account_id,
        COUNT(*) as bug_ticket_count
    FROM support_tickets
    WHERE category = 'bug'
    GROUP BY org_id
)

-- Final aggregation by MRR segment
SELECT 
    as_seg.mrr_segment,
    COUNT(DISTINCT as_seg.account_id) as account_count,
    ROUND(AVG(as_seg.total_mrr)::numeric, 2) as avg_mrr,
    ROUND(MIN(as_seg.total_mrr)::numeric, 2) as min_mrr,
    ROUND(MAX(as_seg.total_mrr)::numeric, 2) as max_mrr,
    COUNT(DISTINCT btc.account_id) as accounts_with_bugs,
    ROUND(100.0 * COUNT(DISTINCT btc.account_id) / COUNT(DISTINCT as_seg.account_id), 2) as bug_reporting_rate,
    COALESCE(SUM(btc.bug_ticket_count), 0) as total_bug_tickets,
    ROUND(COALESCE(AVG(btc.bug_ticket_count), 0)::numeric, 2) as avg_bug_tickets_per_account,
    ROUND(AVG(CASE WHEN btc.bug_ticket_count IS NOT NULL THEN btc.bug_ticket_count END)::numeric, 2) as avg_bug_tickets_per_reporting_account
FROM account_segments as_seg
LEFT JOIN bug_ticket_counts btc ON as_seg.account_id = btc.account_id
GROUP BY as_seg.mrr_segment
ORDER BY 
    CASE as_seg.mrr_segment
        WHEN 'High MRR' THEN 1
        WHEN 'Medium MRR' THEN 2
        WHEN 'Low MRR' THEN 3
        WHEN 'No Subscription' THEN 4
    END;


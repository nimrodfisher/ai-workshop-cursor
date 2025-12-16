# MRR Analysis by Plan - Last 12 Months

## Business Context
> Analysis to understand how Monthly Recurring Revenue (MRR) has changed by subscription plan over the last 12 months. This analysis helps identify which plans are growing, declining, or stable, and informs strategic decisions about plan positioning and pricing.

**Stakeholder(s):** Business Operations Team  
**Date Initiated:** 2024-12-15  
**Status:** Complete

## Business Questions
1. How has MRR changed by plan over the last 12 months?
2. Which plans are showing growth vs. decline?
3. What are the month-over-month trends for each plan?
4. How do the plans compare in terms of total MRR contribution?

## Data Sources
| Source | Table/Dataset | Description | Freshness |
|-----|---|----|-----|
| Supabase | public.subscriptions | Subscription records with monthly pricing and dates | Real-time |
| Supabase | public.accounts | Account information including plan assignments | Real-time |

## Key Definitions
- **MRR (Monthly Recurring Revenue)**: Sum of monthly_price for all active subscriptions in a given month
- **Active Subscription**: A subscription that started before or during the month and was not canceled before the month ended
- **Plan**: Subscription tier assigned to an account (free, pro, enterprise)

## Quick Links
- [HTML Report](./report.html) ⭐ *Interactive report with charts*
- [EDA Report](./eda/eda_report.md)
- [Conclusions](./conclusions/conclusions.md)
- [Queries](./queries/)

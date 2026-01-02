# Bug Ticket User Analysis

## Business Context
> This analysis investigates the characteristics of users and accounts that open support tickets categorized as 'bug_report'. Understanding which user segments are most affected by or reporting bugs helps product and engineering teams prioritize fixes and improve the user experience for key customer segments.

**Stakeholder(s):** Product Management, Engineering, Customer Support  
**Date Initiated:** 2026-01-01  
**Status:** Complete

## Business Questions
1. Which account segments (plan tier, industry) open the most bug-related tickets?
2. Is there a correlation between account age (time since creation) and bug reporting frequency?
3. What user roles are most likely to report bugs?
4. Are bug reports concentrated among a small number of "high-volume" accounts?

## Data Sources
| Source | Table/Dataset | Description | Freshness |
|-----|---|----|-----|
| Supabase | public.support_tickets | Support ticket details including category and reporter | Real-time |
| Supabase | public.accounts | Account-level segments and metadata | Real-time |
| Supabase | public.users | User-level metadata (roles) | Real-time |
| Supabase | public.subscriptions | Subscription status and MRR context | Real-time |

## Key Definitions
- **Bug Ticket**: Any support ticket with `category = 'bug_report'`.
- **Active Account**: An account with at least one active subscription or recent event activity.

## Quick Links
- [📊 PDF Summary Report](./deliverables/report_summary.pdf) - **Complete analysis narrative**
- [🌐 Interactive Dashboard](./deliverables/report_interactive.html) - Filterable charts and tables
- [📄 Static HTML Report](./deliverables/report.html) - Full report with visualizations
- [🗺️ Analysis Flow](./analysis_flow.md) - Visual process map
- [📈 EDA Report](./eda/eda_report.md) - Exploratory data analysis
- [💡 Conclusions](./conclusions/conclusions.md) - Key findings and recommendations
- [🔍 Queries](./queries/) - SQL queries used

### 🎯 Quick Actions
**To generate PDF summary:**
```bash
cd analyses/2026-01-01_bug-ticket-user-analysis
pip install reportlab  # If not already installed
python generate_pdf_summary.py
```

**To view interactive dashboard:** Simply open `deliverables/report_interactive.html` in your browser!


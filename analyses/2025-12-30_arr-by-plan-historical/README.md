# ARR Historical Analysis by Plan

## Business Context
> Analysis to understand how Annual Recurring Revenue (ARR) has evolved over time, broken down by subscription plan tier. This will help identify growth trends, plan performance, and revenue composition changes.

**Stakeholder(s):** Finance/Revenue Team  
**Date Initiated:** 2025-12-30  
**Status:** In Progress

## Business Questions
1. How has total ARR changed over time?
2. How has ARR changed for each plan tier (Free, Pro, Enterprise)?
3. What is the composition of ARR by plan at different points in time?
4. Are there any notable trends or inflection points in ARR growth by plan?

## Data Sources
| Source | Table/Dataset | Description | Freshness |
|--------|---------------|-------------|-----------|
| Supabase | subscriptions | Subscription records with monthly_price, status, dates | Real-time |
| Supabase | accounts | Account information including plan tier | Real-time |

## Key Definitions
- **ARR (Annual Recurring Revenue)**: Total annual value of active recurring subscriptions (monthly_price * 12)
- **Active Subscription**: Subscription with status = 'active'
- **Plan Tier**: The subscription plan level (Free, Pro, Enterprise) from accounts table

## Quick Links

### 📊 Reports (Choose Your Format)
- [🌐 **Interactive Dashboard**](./deliverables/report_interactive.html) - **⭐ START HERE** - Filterable tables, interactive charts, full exploration
- [📄 Static HTML Report](./deliverables/report.html) - Full report with embedded visualizations
- [📊 PDF Summary](./deliverables/report_summary.pdf) - Executive summary (generate with: `python generate_pdf_summary.py`)

### 📋 Supporting Documents
- [🗺️ Analysis Flow](./analysis_flow.md) - Visual mind map of analysis process
- [📈 EDA Report](./eda/eda_report.md) - Exploratory data analysis and validation
- [💡 Conclusions](./conclusions/conclusions.md) - Key findings and actionable recommendations
- [🔍 Queries](./queries/) - SQL queries with full documentation

### 🎯 Quick Actions
**To generate PDF summary:**
```bash
cd analyses/2025-12-30_arr-by-plan-historical
pip install reportlab  # If not already installed
python generate_pdf_summary.py
```

**To view interactive dashboard:** Simply open `deliverables/report_interactive.html` in your browser!

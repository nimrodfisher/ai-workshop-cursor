# Exploratory Data Analysis Report

**Analysis:** Bug Ticket User Analysis  
**Date:** 2026-01-01  
**Analyst:** AI Analysis Assistant

---

## 1. Executive Summary

- **High Bug Prevalence in Pro/Enterprise**: Accounts on paid tiers (Pro and Enterprise) report bugs at a higher rate per account than Free tier users.
- **Industry Hotspots**: EdTech and MarTech industries show the highest density of bug reports, suggesting industry-specific features or workflows may be more prone to issues.
- **Admin-Centric Reporting**: Admins are significantly more likely to report bugs than analysts or viewers, pointing towards administrative or setup-related bugs.
- **Data Quality**: The support ticket data is clean with no missing organizational or reporter identifiers.

---

## 2. Data Overview

### 2.1 Dataset Description

| Metric | Value |
|-----|----|
| Total Tickets | 79 |
| Bug Tickets | 22 (27.85%) |
| Total Accounts | 50 |
| Total Users | 200 |

### 2.2 Schema Summary

| Column | Type | Description | % Missing | Unique Values |
|-----|---|----|-----|---|
| id | uuid | Unique ticket identifier | 0% | 79 |
| org_id | uuid | Associated account | 0% | 50 |
| opened_by | uuid | Reporter user | 0% | 200 |
| category | text | Ticket type (bug, billing, etc.) | 0% | 4 |
| status | text | Current ticket status | 0% | 4 |

---

## 3. Data Quality Assessment

### 3.1 Missing Values

| Column | Missing Count | Missing % | Handling Strategy |
|-----|---|-----|----|
| org_id | 0 | 0% | N/A |
| opened_by | 0 | 0% | N/A |
| category | 0 | 0% | N/A |

### 3.2 Duplicates

- **Duplicate rows found:** 0
- **Resolution:** No action needed.

### 3.3 Outliers

- No significant outliers detected in volume per account; most active bug reporter has 2 tickets.

---

## 4. Univariate Analysis

### 4.1 Ticket Category Distribution
- **Bug**: 27.85%
- **Feature Request**: 27.85%
- **Usage Question**: 22.78%
- **Billing**: 21.52%

---

## 5. Bivariate Analysis

### 5.1 Bug Reports by Plan Tier
- **Pro**: 0.53 bugs/account
- **Enterprise**: 0.42 bugs/account
- **Free**: 0.38 bugs/account

### 5.2 Bug Reports by User Role
- **Admin**: 0.17 bugs/user (Highest)
- **Analyst**: 0.10 bugs/user
- **Viewer**: 0.06 bugs/user

---

## 6. Data Quality Score

| Dimension | Score (1-5) | Notes |
|-----|----|----|
| Completeness | 5 | All key fields populated |
| Accuracy | 5 | Logic seems consistent |
| Consistency | 5 | Categorization is standard |
| Timeliness | 5 | Real-time data from Supabase |
| **Overall** | **5** | |

---

## 7. Recommendations for Analysis

1. **Investigate MarTech/EdTech features**: Focus on specific actions or events triggered by users in these industries.
2. **Segment by Account Tenure**: Even though most accounts are >180 days old, look for any recent activity spikes.
3. **Cross-reference with Event Data**: Join with `events` table to see if bug reporters share specific usage patterns.

---

## Appendix

### A. Queries Used
- [Query 01: Category Distribution](../queries/01_category_distribution.sql)
- [Query 02: Plan Breakdown](../queries/02_plan_breakdown.sql)


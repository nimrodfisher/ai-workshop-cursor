# Analysis Flow: Bug Ticket User Analysis

```mermaid
graph TD
    A[Start: Analysis Request] --> B[Phase 1: Sanity Checks]
    B --> C[Phase 2: EDA & Data Quality]
    C --> D{Checkpoint 1: Data Validated?}
    D -- No --> E[Investigate Data Issues]
    E --> C
    D -- Yes --> F[Phase 3: Main Analysis]
    F --> G[Segment Analysis: Plan, Industry, Role]
    G --> H[Temporal Analysis: Account Age vs. Bugs]
    H --> I[Volume Analysis: Account Concentration]
    I --> J{Checkpoint 2: Insights Complete?}
    J -- No --> F
    J -- Yes --> K[Phase 4: Synthesis & Conclusions]
    K --> L[Phase 5: Report Generation]
    L --> M[Checkpoint 3: Deliverables Ready]
    M --> N[End: Analysis Delivered]
```

## Step-by-Step Flow

1. **Setup**: Create folder structure and documentation.
2. **Phase 1: Sanity Checks**: Validate counts and basic distributions for `support_tickets`, `accounts`, and `users`.
3. **Phase 2: EDA**:
    - Analyze distribution of ticket categories.
    - Check for missing values in `opened_by` and `org_id`.
    - Profile bug reporting volume over time.
4. **Phase 3: Main Analysis**:
    - **Query 01**: Breakdown of bug tickets by Account Plan Tier.
    - **Query 02**: Breakdown of bug tickets by Industry.
    - **Query 03**: Correlation between Account Age and Bug Reporting.
    - **Query 04**: Breakdown of bug tickets by User Role.
    - **Query 05**: Identification of "Power Bug Reporters" (top accounts).
5. **Phase 4: Synthesis**: Summarize findings in `conclusions.md`.
6. **Phase 5: Deliverables**: Generate branded HTML and PDF reports.


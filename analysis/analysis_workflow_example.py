"""
Example Analysis Workflow demonstrating:
- Performance-aware querying
- Validation after aggregations
- Gradual transparent process
- Context from schema + user input + real-time data
"""

from analysis_framework import AnalysisFramework
from context_manager import ContextManager
from datetime import datetime, timedelta

def example_analysis():
    """
    Example: Analyze MRR by plan with full transparency and validation
    """
    
    # Initialize context manager
    context = ContextManager(
        github_owner="nimrodfisher",
        github_repo="workshop-queries-repo"
    )
    
    # Load schema from GitHub
    print("📚 Loading schema context from GitHub...")
    context.load_schema_from_github("schema.yml")
    
    # Add user question
    user_question = "What's our Monthly Recurring Revenue (MRR) broken down by plan?"
    context.add_user_context(user_question)
    
    # Map question to schema
    mapping = context.map_user_question_to_schema(user_question)
    print(f"\n🔍 Context mapping:")
    print(f"   Tables identified: {[t['name'] for t in mapping['tables']]}")
    print(f"   Metrics identified: {[m['name'] for m in mapping['metrics']]}")
    
    # Initialize analysis framework
    framework = AnalysisFramework(schema_context=context.schema_context)
    framework.connect()
    
    try:
        print("\n" + "="*80)
        print("ANALYSIS WORKFLOW: MRR by Plan")
        print("="*80)
        
        # STEP 1: Understand the data - Check subscriptions table
        print("\n🔍 STEP 1: Understanding the data...")
        step1 = framework.add_step(
            description="First, let's check if we have subscription data and understand its structure",
            query="""
                SELECT 
                    COUNT(*) as total_subscriptions,
                    COUNT(DISTINCT org_id) as unique_accounts,
                    COUNT(DISTINCT status) as status_types
                FROM subscriptions;
            """,
            assumptions=[
                "We're looking at all subscriptions, not just active ones",
                "Each subscription belongs to one account (org_id)"
            ],
            clarifications=[
                "Should we include canceled subscriptions in the analysis?",
                "Do we want to filter by a specific date range?"
            ]
        )
        framework.print_step_summary(step1)
        
        # STEP 2: Check key dimensions - What plans exist?
        print("\n🔍 STEP 2: Identifying key dimensions...")
        step2 = framework.add_step(
            description="Let's see what subscription plans exist in the accounts table",
            query="""
                SELECT 
                    plan,
                    COUNT(*) as account_count
                FROM accounts
                WHERE plan IS NOT NULL
                GROUP BY plan
                ORDER BY account_count DESC;
            """,
            assumptions=[
                "Plan information is stored in the accounts table",
                "Some accounts might not have a plan assigned (NULL values)"
            ]
        )
        framework.print_step_summary(step2)
        
        # STEP 3: Calculate basic MRR
        print("\n🔍 STEP 3: Calculating basic MRR...")
        step3 = framework.add_step(
            description="Calculate total MRR from active subscriptions",
            query="""
                SELECT 
                    SUM(monthly_price) as total_mrr,
                    COUNT(*) as active_subscription_count,
                    AVG(monthly_price) as avg_monthly_price
                FROM subscriptions
                WHERE status = 'active';
            """,
            assumptions=[
                "Only 'active' status subscriptions contribute to MRR",
                "monthly_price represents the recurring revenue amount"
            ],
            clarifications=[
                "Should we include subscriptions with status 'trial' or 'paused'?",
                "Are there any prorated subscriptions we should account for?"
            ]
        )
        framework.print_step_summary(step3)
        
        # STEP 4: MRR by plan (with validation)
        print("\n🔍 STEP 4: Calculating MRR by plan (with validation)...")
        step4 = framework.add_step(
            description="Break down MRR by account plan - this creates a new segmentation",
            query="""
                SELECT 
                    a.plan,
                    COUNT(s.id) as subscription_count,
                    SUM(s.monthly_price) as mrr,
                    AVG(s.monthly_price) as avg_price_per_subscription
                FROM subscriptions s
                JOIN accounts a ON s.org_id = a.id
                WHERE s.status = 'active'
                  AND a.plan IS NOT NULL
                GROUP BY a.plan
                ORDER BY mrr DESC;
            """,
            assumptions=[
                "Each subscription is linked to an account via org_id",
                "We only count subscriptions where the account has a plan assigned",
                "Active subscriptions are those with status = 'active'"
            ],
            clarifications=[
                "Should we handle accounts with NULL plans differently?",
                "Do we want to see MRR trends over time or just current snapshot?"
            ],
            validate=True,  # Enable validation
            aggregation_column="mrr",
            segment_columns=["plan"],
            table_name="subscriptions"
        )
        framework.print_step_summary(step4)
        
        # STEP 5: Additional context - Check data quality
        print("\n🔍 STEP 5: Data quality check...")
        step5 = framework.add_step(
            description="Check for potential data quality issues that might affect our analysis",
            query="""
                SELECT 
                    COUNT(*) as total_subscriptions,
                    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_count,
                    COUNT(CASE WHEN monthly_price IS NULL THEN 1 END) as null_price_count,
                    COUNT(CASE WHEN org_id IS NULL THEN 1 END) as null_org_count,
                    COUNT(CASE WHEN status = 'active' AND monthly_price <= 0 THEN 1 END) as invalid_price_count
                FROM subscriptions;
            """,
            assumptions=[
                "Subscriptions with NULL or zero prices might indicate data quality issues"
            ]
        )
        framework.print_step_summary(step5)
        
        # Print final summary
        print("\n" + "="*80)
        print("ANALYSIS SUMMARY")
        print("="*80)
        summary = framework.get_analysis_summary()
        print(f"Total steps: {summary['total_steps']}")
        print(f"Total execution time: {summary['total_execution_time']:.3f} seconds")
        print(f"\nSteps completed:")
        for step_info in summary['steps']:
            validation_status = ""
            if step_info['has_validation']:
                status = "✓" if step_info['validation_passed'] else "✗"
                validation_status = f" [{status} validated]"
            print(f"  Step {step_info['step_number']}: {step_info['description'][:50]}... "
                  f"({step_info['row_count']} rows, {step_info['execution_time']:.3f}s){validation_status}")
        
        # Print context summary
        print("\n" + context.build_context_summary())
        
    finally:
        framework.close()


if __name__ == "__main__":
    example_analysis()




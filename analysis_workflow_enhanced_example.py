"""
Enhanced Analysis Workflow Example
Demonstrates all new features:
- Sanity checks
- EDA
- Text classification
- Diagnostic analysis and segment comparison
"""

from analysis_framework import AnalysisFramework
from context_manager import ContextManager


def enhanced_analysis_example():
    """
    Complete example showing all analysis phases
    """
    
    # Initialize context manager
    context = ContextManager(
        github_owner="nimrodfisher",
        github_repo="workshop-queries-repo"
    )
    
    # Load schema from GitHub
    print("📚 Loading schema context from GitHub...")
    context.load_schema_from_github("schema.yml")
    
    # Initialize analysis framework
    framework = AnalysisFramework(schema_context=context.schema_context)
    framework.connect()
    
    try:
        print("\n" + "="*80)
        print("ENHANCED ANALYSIS WORKFLOW")
        print("="*80)
        
        # PHASE 1: Sanity Checks
        print("\n🔍 PHASE 1: Sanity Checks")
        print("-" * 80)
        
        # Run sanity checks on users table
        sanity_results = framework.run_sanity_checks("users")
        
        # Run sanity checks on subscriptions table
        sanity_results = framework.run_sanity_checks("subscriptions")
        
        # PHASE 2: EDA (Exploratory Data Analysis)
        print("\n📊 PHASE 2: Exploratory Data Analysis")
        print("-" * 80)
        
        # Run EDA on users table
        eda_results = framework.run_eda("users", sample_size=1000)
        
        # Run EDA on events table (sample for performance)
        eda_results = framework.run_eda("events", sample_size=5000)
        
        # PHASE 3: Main Analysis with Validation
        print("\n📈 PHASE 3: Main Analysis")
        print("-" * 80)
        
        # Calculate MRR by plan
        step = framework.add_step(
            description="Calculate MRR by plan",
            query="""
                SELECT 
                    a.plan,
                    COUNT(s.id) as subscription_count,
                    SUM(s.monthly_price) as mrr
                FROM subscriptions s
                JOIN accounts a ON s.org_id = a.id
                WHERE s.status = 'active'
                  AND a.plan IS NOT NULL
                GROUP BY a.plan
                ORDER BY mrr DESC;
            """,
            assumptions=["Only active subscriptions count"],
            validate=True,
            aggregation_column="mrr",
            segment_columns=["plan"],
            table_name="subscriptions"
        )
        framework.print_step_summary(step)
        
        # PHASE 4: Text Classification (if needed)
        print("\n🏷️  PHASE 4: Text Classification (Optional)")
        print("-" * 80)
        
        # Example: Classify support ticket categories
        # Uncomment if you have text data to classify
        # classification_results = framework.classify_text_column(
        #     table_name="support_tickets",
        #     column_name="category",
        #     user_context="Classify support tickets by urgency and type",
        #     num_categories=5
        # )
        
        # PHASE 5: Diagnostic Analysis and Segment Comparison
        print("\n🔬 PHASE 5: Diagnostic Analysis and Segment Comparison")
        print("-" * 80)
        
        # Compare MRR across different segments
        diagnostic_results = framework.run_diagnostic_analysis(
            query="""
                SELECT 
                    a.plan,
                    a.industry,
                    s.monthly_price,
                    s.status
                FROM subscriptions s
                JOIN accounts a ON s.org_id = a.id
                WHERE s.status = 'active'
                  AND a.plan IS NOT NULL
                  AND a.industry IS NOT NULL;
            """,
            target_column="monthly_price",
            segment_columns=["plan", "industry"],
            description="Compare subscription prices across plans and industries"
        )
        
        # Final Summary
        print("\n" + "="*80)
        print("ANALYSIS SUMMARY")
        print("="*80)
        summary = framework.get_analysis_summary()
        print(f"Total steps: {summary['total_steps']}")
        print(f"Total execution time: {summary['total_execution_time']:.3f} seconds")
        print(f"\nSteps completed:")
        for step_info in summary['steps']:
            step_type = "Sanity Check" if "sanity" in step_info['description'].lower() else \
                       "EDA" if "exploratory" in step_info['description'].lower() else \
                       "Diagnostic" if "diagnostic" in step_info['description'].lower() else \
                       "Analysis"
            print(f"  {step_info['step_number']}. [{step_type}] {step_info['description'][:50]}...")
        
    finally:
        framework.close()


if __name__ == "__main__":
    enhanced_analysis_example()


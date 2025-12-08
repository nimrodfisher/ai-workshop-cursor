"""
Analysis Runner - Main interface for running analysis in Cursor chat
This is the primary entry point for analysis workflows
"""

from analysis_framework import AnalysisFramework
from context_manager import ContextManager
from html_dashboard_generator import HTMLDashboardGenerator, create_dashboard_from_analysis
from typing import Dict, List, Any, Optional
import os


class AnalysisRunner:
    """
    Main runner for analysis workflows in Cursor
    Handles the complete flow: context → analysis → dashboard (if requested)
    """
    
    def __init__(self, github_owner: str = "nimrodfisher", github_repo: str = "workshop-queries-repo"):
        self.context = ContextManager(github_owner, github_repo)
        self.framework = None
        self.analysis_results = None
        
    def initialize(self):
        """Initialize the analysis environment"""
        # Load schema from GitHub
        print("📚 Loading schema context from GitHub...")
        self.context.load_schema_from_github("schema.yml")
        
        # Initialize framework
        self.framework = AnalysisFramework(schema_context=self.context.schema_context)
        self.framework.connect()
        
        print("✅ Analysis framework initialized")
    
    def run_analysis(self, question: str, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Run a complete analysis workflow
        
        Args:
            question: User's analysis question
            steps: List of step definitions with:
                - description: What this step does
                - query: SQL query
                - assumptions: List of assumptions
                - clarifications: List of clarification questions
                - validate: Whether to validate (if aggregation)
                - aggregation_column: Column being aggregated
                - segment_columns: Columns for grouping
                - table_name: Base table name
        """
        # Add user context
        self.context.add_user_context(question)
        
        # Map question to schema
        mapping = self.context.map_user_question_to_schema(question)
        
        print(f"\n🔍 Analysis Question: {question}")
        print(f"📊 Tables identified: {[t['name'] for t in mapping['tables']]}")
        if mapping.get('metrics'):
            print(f"📈 Metrics identified: {[m['name'] for m in mapping['metrics']]}")
        
        # Execute each step
        for step_def in steps:
            step = self.framework.add_step(**step_def)
            self.framework.print_step_summary(step)
        
        # Get summary
        self.analysis_results = self.framework.get_analysis_summary()
        self.analysis_results['question'] = question
        self.analysis_results['context_mapping'] = mapping
        
        return self.analysis_results
    
    def create_dashboard(self, dashboard_config: Optional[Dict[str, Any]] = None) -> str:
        """
        Create HTML dashboard from analysis results
        
        Args:
            dashboard_config: Optional configuration for dashboard
                - title: Dashboard title
                - include_metrics: List of metrics to include
                - include_charts: List of charts to include
                - include_tables: List of tables to include
        
        Returns:
            Path to saved HTML file
        """
        if not self.analysis_results:
            raise ValueError("No analysis results available. Run analysis first.")
        
        generator = HTMLDashboardGenerator()
        
        # Set title
        title = dashboard_config.get('title', 'Analysis Dashboard') if dashboard_config else 'Analysis Dashboard'
        generator.title = title
        generator.description = f"Analysis: {self.analysis_results.get('question', 'N/A')}"
        
        # Add metrics
        if dashboard_config and dashboard_config.get('include_metrics'):
            for metric in dashboard_config['include_metrics']:
                generator.add_metric(**metric)
        else:
            # Default: add summary metrics
            generator.add_metric(
                label="Total Steps",
                value=self.analysis_results['total_steps'],
                format="number"
            )
            generator.add_metric(
                label="Execution Time",
                value=f"{self.analysis_results['total_execution_time']:.2f}s",
                format="number"
            )
        
        # Add charts
        if dashboard_config and dashboard_config.get('include_charts'):
            for chart in dashboard_config['include_charts']:
                generator.add_chart(**chart)
        
        # Add tables
        if dashboard_config and dashboard_config.get('include_tables'):
            for table in dashboard_config['include_tables']:
                generator.add_table(**table)
        
        # Save dashboard
        from datetime import datetime
        filepath = f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        generator.save_dashboard(filepath)
        
        print(f"\n✅ Dashboard created: {filepath}")
        print(f"📂 Open in browser to view")
        
        return filepath
    
    def cleanup(self):
        """Clean up resources"""
        if self.framework:
            self.framework.close()


# Convenience function for quick analysis
def quick_analysis(question: str, query: str, description: str = None) -> Dict[str, Any]:
    """
    Quick analysis helper for simple queries
    
    Args:
        question: User's question
        query: SQL query to execute
        description: Optional description of what the query does
    
    Returns:
        Analysis results
    """
    runner = AnalysisRunner()
    runner.initialize()
    
    try:
        steps = [{
            'description': description or f"Answer: {question}",
            'query': query
        }]
        
        results = runner.run_analysis(question, steps)
        return results
    finally:
        runner.cleanup()


# Example usage patterns
if __name__ == "__main__":
    # Example 1: Simple analysis
    print("Example: Simple count query")
    results = quick_analysis(
        question="How many users do we have?",
        query="SELECT COUNT(*) as user_count FROM users;",
        description="Count total users in the database"
    )
    
    # Example 2: Full workflow with dashboard
    print("\n" + "="*80)
    print("Example: Full workflow with dashboard creation")
    print("="*80)
    
    runner = AnalysisRunner()
    runner.initialize()
    
    try:
        # Run analysis
        steps = [
            {
                'description': "Count total users",
                'query': "SELECT COUNT(*) as count FROM users;"
            },
            {
                'description': "Count users by role",
                'query': """
                    SELECT role, COUNT(*) as count
                    FROM users
                    WHERE role IS NOT NULL
                    GROUP BY role;
                """,
                'validate': True,
                'aggregation_column': 'count',
                'segment_columns': ['role'],
                'table_name': 'users'
            }
        ]
        
        results = runner.run_analysis("How many users do we have by role?", steps)
        
        # Create dashboard
        dashboard_config = {
            'title': 'User Analysis Dashboard',
            'include_metrics': [
                {
                    'label': 'Total Users',
                    'value': results['steps'][0]['row_count'],
                    'format': 'number'
                }
            ]
        }
        
        dashboard_path = runner.create_dashboard(dashboard_config)
        print(f"\n✅ Complete! Dashboard saved to: {dashboard_path}")
        
    finally:
        runner.cleanup()




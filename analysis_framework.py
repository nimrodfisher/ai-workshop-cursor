"""
Analysis Framework with Performance, Validation, and Gradual Process
Implements transparent step-by-step analysis with validation checks
"""

import psycopg
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class AnalysisStep:
    """Represents a single step in the analysis process"""
    step_number: int
    description: str
    query: str
    assumptions: List[str] = field(default_factory=list)
    clarifications_needed: List[str] = field(default_factory=list)
    validation_results: Dict[str, Any] = field(default_factory=dict)
    execution_time: Optional[float] = None
    row_count: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationCase:
    """Represents a validation case for checking aggregations"""
    case_id: str
    description: str
    raw_data_query: str
    expected_value: Optional[Any] = None
    actual_value: Optional[Any] = None
    passed: Optional[bool] = None
    notes: str = ""


class AnalysisFramework:
    """
    Main analysis framework that implements:
    - Performance-aware querying based on metadata
    - Validation after aggregations
    - Gradual transparent process
    - Context from schema + user input + real-time data
    """
    
    def __init__(self, schema_context: Optional[Dict] = None):
        self.schema_context = schema_context or {}
        self.steps: List[AnalysisStep] = []
        self.connection = None
        self.table_metadata: Dict[str, Dict] = {}
        
    def connect(self):
        """Establish database connection"""
        self.connection = psycopg.connect(
            host=os.getenv("SUPABASE_HOST"),
            port=os.getenv("SUPABASE_PORT", "5432"),
            dbname=os.getenv("SUPABASE_DB"),
            user=os.getenv("SUPABASE_USER"),
            password=os.getenv("SUPABASE_PASSWORD")
        )
        
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    def get_table_metadata(self, table_name: str) -> Dict[str, Any]:
        """
        Get metadata about a table for performance optimization
        Returns: row count, column info, indexes, etc.
        """
        if table_name in self.table_metadata:
            return self.table_metadata[table_name]
        
        metadata_query = f"""
            SELECT 
                COUNT(*) as row_count,
                pg_size_pretty(pg_total_relation_size('{table_name}')) as table_size
            FROM {table_name};
        """
        
        # Get column information
        column_query = f"""
            SELECT 
                column_name,
                data_type,
                is_nullable
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position;
        """
        
        try:
            row_count_df = pd.read_sql_query(metadata_query, self.connection)
            columns_df = pd.read_sql_query(column_query, self.connection)
            
            metadata = {
                'row_count': int(row_count_df['row_count'].iloc[0]),
                'table_size': row_count_df['table_size'].iloc[0],
                'columns': columns_df.to_dict('records'),
                'last_checked': datetime.now().isoformat()
            }
            
            self.table_metadata[table_name] = metadata
            return metadata
            
        except Exception as e:
            return {
                'row_count': None,
                'error': str(e),
                'columns': []
            }
    
    def check_performance_considerations(self, query: str, tables: List[str]) -> Dict[str, Any]:
        """
        Analyze query performance based on metadata
        Returns performance recommendations
        """
        considerations = {
            'warnings': [],
            'recommendations': [],
            'estimated_cost': 'low'
        }
        
        for table in tables:
            metadata = self.get_table_metadata(table)
            row_count = metadata.get('row_count', 0)
            
            # Large table warnings
            if row_count and row_count > 1000000:
                considerations['warnings'].append(
                    f"Large table detected: {table} has {row_count:,} rows. "
                    "Consider adding date filters or LIMIT clauses."
                )
                considerations['estimated_cost'] = 'high'
            elif row_count and row_count > 100000:
                considerations['warnings'].append(
                    f"Medium table: {table} has {row_count:,} rows. "
                    "Consider filtering for better performance."
                )
                considerations['estimated_cost'] = 'medium'
            
            # Check for date filters on time-series tables
            if any(col['column_name'] in ['created_at', 'occurred_at', 'timestamp'] 
                   for col in metadata.get('columns', [])):
                if 'WHERE' in query.upper() and any(
                    date_col in query.upper() 
                    for date_col in ['created_at', 'occurred_at', 'timestamp']
                ):
                    considerations['recommendations'].append(
                        f"Good: Date filter detected for {table}"
                    )
                else:
                    considerations['warnings'].append(
                        f"Consider adding date filter for {table} to improve performance"
                    )
        
        return considerations
    
    def execute_query(self, query: str, explain: bool = True) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Execute query with performance monitoring
        Returns: (DataFrame, execution metadata)
        """
        start_time = datetime.now()
        
        # Get EXPLAIN plan if requested
        explain_info = {}
        if explain:
            try:
                explain_query = f"EXPLAIN (FORMAT JSON) {query}"
                explain_df = pd.read_sql_query(explain_query, self.connection)
                if not explain_df.empty:
                    explain_info = json.loads(explain_df.iloc[0, 0])[0]
            except:
                pass
        
        # Execute main query
        result_df = pd.read_sql_query(query, self.connection)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        metadata = {
            'execution_time': execution_time,
            'row_count': len(result_df),
            'columns': list(result_df.columns),
            'explain_plan': explain_info
        }
        
        return result_df, metadata
    
    def validate_aggregation(
        self, 
        aggregation_query: str,
        aggregation_column: str,
        segment_columns: List[str],
        table_name: str,
        num_cases: int = 3
    ) -> List[ValidationCase]:
        """
        Validate aggregation by checking 2-3 raw data cases
        
        Args:
            aggregation_query: The aggregation query to validate
            aggregation_column: The column being aggregated (e.g., 'count', 'sum')
            segment_columns: Columns used for grouping/segmentation
            table_name: Base table name
            num_cases: Number of validation cases to check
        """
        validation_cases = []
        
        # First, get the aggregated results
        agg_df, _ = self.execute_query(aggregation_query, explain=False)
        
        # Select a few segments to validate
        sample_segments = agg_df.head(num_cases)
        
        for idx, segment_row in sample_segments.iterrows():
            # Build WHERE clause for this segment
            where_conditions = []
            for col in segment_columns:
                if col in segment_row and pd.notna(segment_row[col]):
                    if isinstance(segment_row[col], str):
                        where_conditions.append(f"{col} = '{segment_row[col]}'")
                    else:
                        where_conditions.append(f"{col} = {segment_row[col]}")
            
            where_clause = " AND ".join(where_conditions)
            
            # Query raw data for this segment
            raw_data_query = f"""
                SELECT * 
                FROM {table_name}
                WHERE {where_clause}
                LIMIT 100;
            """
            
            raw_df, _ = self.execute_query(raw_data_query, explain=False)
            
            # Calculate expected aggregation manually
            if aggregation_column.lower() in ['count', 'count(*)']:
                expected = len(raw_df)
            elif 'sum' in aggregation_column.lower():
                sum_col = aggregation_column.replace('SUM(', '').replace(')', '').strip()
                expected = raw_df[sum_col].sum() if sum_col in raw_df.columns else None
            elif 'avg' in aggregation_column.lower():
                avg_col = aggregation_column.replace('AVG(', '').replace(')', '').strip()
                expected = raw_df[avg_col].mean() if avg_col in raw_df.columns else None
            else:
                expected = None
            
            actual = segment_row[aggregation_column]
            
            # Check if validation passed
            passed = None
            if expected is not None and actual is not None:
                # Allow small floating point differences
                if isinstance(expected, float) and isinstance(actual, float):
                    passed = abs(expected - actual) < 0.01
                else:
                    passed = expected == actual
            
            validation_case = ValidationCase(
                case_id=f"case_{idx + 1}",
                description=f"Validation for segment: {dict(segment_row[segment_columns])}",
                raw_data_query=raw_data_query,
                expected_value=expected,
                actual_value=actual,
                passed=passed,
                notes=f"Checked {len(raw_df)} raw records"
            )
            
            validation_cases.append(validation_case)
        
        return validation_cases
    
    def add_step(
        self,
        description: str,
        query: str,
        assumptions: List[str] = None,
        clarifications: List[str] = None,
        validate: bool = False,
        aggregation_column: str = None,
        segment_columns: List[str] = None,
        table_name: str = None
    ) -> AnalysisStep:
        """
        Add a new analysis step with full transparency
        
        Args:
            description: Plain language description of what this step does
            query: SQL query to execute
            assumptions: List of assumptions made
            clarifications: Questions that need user clarification
            validate: Whether to validate this step (if it's an aggregation)
            aggregation_column: Column being aggregated (for validation)
            segment_columns: Columns used for grouping (for validation)
            table_name: Base table name (for validation)
        """
        step_num = len(self.steps) + 1
        
        # Extract table names from query
        tables = self._extract_table_names(query)
        
        # Check performance
        perf_considerations = self.check_performance_considerations(query, tables)
        
        # Execute query
        result_df, metadata = self.execute_query(query)
        
        # Create step
        step = AnalysisStep(
            step_number=step_num,
            description=description,
            query=query,
            assumptions=assumptions or [],
            clarifications_needed=clarifications or [],
            execution_time=metadata['execution_time'],
            row_count=metadata['row_count'],
            metadata={
                'performance': perf_considerations,
                'columns': metadata['columns'],
                'tables_used': tables
            }
        )
        
        # Validate if requested
        if validate and aggregation_column and segment_columns and table_name:
            validation_cases = self.validate_aggregation(
                query, aggregation_column, segment_columns, table_name
            )
            step.validation_results = {
                'cases': [
                    {
                        'case_id': case.case_id,
                        'description': case.description,
                        'passed': case.passed,
                        'expected': case.expected_value,
                        'actual': case.actual_value,
                        'notes': case.notes
                    }
                    for case in validation_cases
                ],
                'all_passed': all(c.passed for c in validation_cases if c.passed is not None)
            }
        
        self.steps.append(step)
        return step
    
    def _extract_table_names(self, query: str) -> List[str]:
        """Extract table names from SQL query"""
        import re
        # Simple extraction - looks for FROM and JOIN clauses
        tables = []
        from_matches = re.findall(r'FROM\s+(\w+)', query, re.IGNORECASE)
        join_matches = re.findall(r'JOIN\s+(\w+)', query, re.IGNORECASE)
        tables.extend(from_matches)
        tables.extend(join_matches)
        return list(set(tables))
    
    def print_step_summary(self, step: AnalysisStep):
        """Print a transparent summary of the analysis step"""
        print(f"\n{'='*80}")
        print(f"STEP {step.step_number}: {step.description}")
        print(f"{'='*80}")
        
        print(f"\n📊 What this step does:")
        print(f"   {step.description}")
        
        if step.assumptions:
            print(f"\n⚠️  Assumptions made:")
            for assumption in step.assumptions:
                print(f"   • {assumption}")
        
        if step.clarifications_needed:
            print(f"\n❓ Clarifications needed:")
            for clarification in step.clarifications_needed:
                print(f"   • {clarification}")
        
        print(f"\n🔍 Query executed:")
        print(f"   {step.query[:200]}..." if len(step.query) > 200 else f"   {step.query}")
        
        print(f"\n📈 Results:")
        print(f"   • Rows returned: {step.row_count:,}")
        print(f"   • Execution time: {step.execution_time:.3f} seconds")
        print(f"   • Columns: {', '.join(step.metadata.get('columns', []))}")
        
        # Performance warnings
        perf = step.metadata.get('performance', {})
        if perf.get('warnings'):
            print(f"\n⚠️  Performance warnings:")
            for warning in perf['warnings']:
                print(f"   • {warning}")
        
        if perf.get('recommendations'):
            print(f"\n💡 Performance recommendations:")
            for rec in perf['recommendations']:
                print(f"   • {rec}")
        
        # Validation results
        if step.validation_results:
            print(f"\n✅ Validation results:")
            for case in step.validation_results.get('cases', []):
                status = "✓ PASSED" if case['passed'] else "✗ FAILED" if case['passed'] is False else "? UNKNOWN"
                print(f"   {status}: {case['description']}")
                if case['expected'] is not None:
                    print(f"      Expected: {case['expected']}, Actual: {case['actual']}")
                print(f"      {case['notes']}")
            
            if step.validation_results.get('all_passed'):
                print(f"\n   ✅ All validation cases passed!")
            else:
                print(f"\n   ⚠️  Some validation cases failed or need review")
        
        print(f"\n{'='*80}\n")
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get complete summary of the analysis"""
        return {
            'total_steps': len(self.steps),
            'total_execution_time': sum(s.execution_time or 0 for s in self.steps),
            'steps': [
                {
                    'step_number': s.step_number,
                    'description': s.description,
                    'row_count': s.row_count,
                    'execution_time': s.execution_time,
                    'has_validation': bool(s.validation_results),
                    'validation_passed': s.validation_results.get('all_passed') if s.validation_results else None
                }
                for s in self.steps
            ]
        }



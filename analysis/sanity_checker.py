"""
Sanity Check Module
Performs data quality checks based on sanity_check_rules.yml
"""

import yaml
import pandas as pd
from typing import Dict, List, Any, Optional
import psycopg
from datetime import datetime


class SanityChecker:
    """
    Performs data quality sanity checks on tables
    """
    
    def __init__(self, connection, rules_file: str = "sanity_check_rules.yml"):
        self.connection = connection
        self.rules = self._load_rules(rules_file)
        self.check_results: List[Dict[str, Any]] = []
        
    def _load_rules(self, rules_file: str) -> Dict[str, Any]:
        """Load sanity check rules from YAML file"""
        try:
            with open(rules_file, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Warning: {rules_file} not found. Using default rules.")
            return {}
        except Exception as e:
            print(f"Error loading rules: {e}")
            return {}
    
    def run_sanity_checks(self, table_name: str) -> Dict[str, Any]:
        """
        Run all sanity checks for a table
        
        Returns:
            Dictionary with check results organized by category
        """
        results = {
            'table_name': table_name,
            'timestamp': datetime.now().isoformat(),
            'null_checks': [],
            'duplicate_checks': [],
            'consistency_checks': [],
            'completeness_checks': [],
            'summary': {
                'total_checks': 0,
                'passed': 0,
                'warnings': 0,
                'errors': 0
            }
        }
        
        # Get table-specific rules
        table_rules = self.rules.get('table_specific_rules', {}).get(table_name, {})
        
        # Run null checks
        if self.rules.get('sanity_checks', {}).get('null_checks', {}).get('enabled', True):
            results['null_checks'] = self._check_nulls(table_name, table_rules)
        
        # Run duplicate checks
        if self.rules.get('sanity_checks', {}).get('duplicate_checks', {}).get('enabled', True):
            results['duplicate_checks'] = self._check_duplicates(table_name, table_rules)
        
        # Run consistency checks
        if self.rules.get('sanity_checks', {}).get('consistency_checks', {}).get('enabled', True):
            results['consistency_checks'] = self._check_consistency(table_name, table_rules)
        
        # Run completeness checks
        if self.rules.get('sanity_checks', {}).get('completeness_checks', {}).get('enabled', True):
            results['completeness_checks'] = self._check_completeness(table_name, table_rules)
        
        # Calculate summary
        for category in ['null_checks', 'duplicate_checks', 'consistency_checks', 'completeness_checks']:
            for check in results[category]:
                results['summary']['total_checks'] += 1
                if check.get('status') == 'passed':
                    results['summary']['passed'] += 1
                elif check.get('severity') == 'warning':
                    results['summary']['warnings'] += 1
                elif check.get('severity') == 'error':
                    results['summary']['errors'] += 1
        
        self.check_results.append(results)
        return results
    
    def _check_nulls(self, table_name: str, table_rules: Dict) -> List[Dict[str, Any]]:
        """Check for null values"""
        checks = []
        
        # Get critical columns
        critical_columns = table_rules.get('critical_columns', [])
        required_columns = table_rules.get('required_columns', [])
        
        # Check critical columns
        for col in critical_columns:
            query = f"""
                SELECT 
                    COUNT(*) as total_rows,
                    COUNT({col}) as non_null_count,
                    COUNT(*) - COUNT({col}) as null_count,
                    ROUND(100.0 * (COUNT(*) - COUNT({col})) / COUNT(*), 2) as null_percentage
                FROM {table_name};
            """
            
            try:
                df = pd.read_sql_query(query, self.connection)
                null_count = int(df['null_count'].iloc[0])
                null_pct = float(df['null_percentage'].iloc[0])
                
                status = 'passed' if null_count == 0 else 'failed'
                severity = 'error' if null_count > 0 else 'info'
                
                checks.append({
                    'check_name': f'null_check_{col}',
                    'column': col,
                    'null_count': null_count,
                    'null_percentage': null_pct,
                    'status': status,
                    'severity': severity,
                    'message': f"Column '{col}' has {null_count} null values ({null_pct}%)"
                })
            except Exception as e:
                checks.append({
                    'check_name': f'null_check_{col}',
                    'column': col,
                    'status': 'error',
                    'severity': 'error',
                    'message': f"Error checking nulls: {str(e)}"
                })
        
        return checks
    
    def _check_duplicates(self, table_name: str, table_rules: Dict) -> List[Dict[str, Any]]:
        """Check for duplicate records"""
        checks = []
        
        # Check primary key duplicates (shouldn't happen, but check anyway)
        query = f"""
            SELECT COUNT(*) as total_rows,
                   COUNT(DISTINCT id) as unique_ids
            FROM {table_name};
        """
        
        try:
            df = pd.read_sql_query(query, self.connection)
            total = int(df['total_rows'].iloc[0])
            unique = int(df['unique_ids'].iloc[0])
            duplicates = total - unique
            
            status = 'passed' if duplicates == 0 else 'failed'
            severity = 'error' if duplicates > 0 else 'info'
            
            checks.append({
                'check_name': 'primary_key_duplicates',
                'total_rows': total,
                'unique_ids': unique,
                'duplicate_count': duplicates,
                'status': status,
                'severity': severity,
                'message': f"Found {duplicates} duplicate primary keys" if duplicates > 0 else "No duplicate primary keys"
            })
        except Exception as e:
            checks.append({
                'check_name': 'primary_key_duplicates',
                'status': 'error',
                'severity': 'error',
                'message': f"Error checking duplicates: {str(e)}"
            })
        
        # Check business key duplicates
        business_keys = table_rules.get('business_keys', [])
        for key in business_keys:
            if '.' in key:
                col = key.split('.')[-1]
            else:
                col = key
            
            query = f"""
                SELECT 
                    {col},
                    COUNT(*) as count
                FROM {table_name}
                WHERE {col} IS NOT NULL
                GROUP BY {col}
                HAVING COUNT(*) > 1
                LIMIT 10;
            """
            
            try:
                df = pd.read_sql_query(query, self.connection)
                duplicate_count = len(df)
                
                status = 'passed' if duplicate_count == 0 else 'failed'
                severity = 'warning' if duplicate_count > 0 else 'info'
                
                checks.append({
                    'check_name': f'business_key_duplicates_{col}',
                    'column': col,
                    'duplicate_count': duplicate_count,
                    'status': status,
                    'severity': severity,
                    'message': f"Found {duplicate_count} duplicate values in '{col}'" if duplicate_count > 0 else f"No duplicates in '{col}'"
                })
            except Exception as e:
                checks.append({
                    'check_name': f'business_key_duplicates_{col}',
                    'column': col,
                    'status': 'error',
                    'severity': 'error',
                    'message': f"Error checking duplicates: {str(e)}"
                })
        
        return checks
    
    def _check_consistency(self, table_name: str, table_rules: Dict) -> List[Dict[str, Any]]:
        """Check for data consistency issues"""
        checks = []
        
        # Check date ranges
        date_ranges = table_rules.get('date_ranges', [])
        for date_range in date_ranges:
            start_col = date_range.get('start')
            end_col = date_range.get('end')
            
            if start_col and end_col:
                query = f"""
                    SELECT COUNT(*) as invalid_ranges
                    FROM {table_name}
                    WHERE {start_col} IS NOT NULL 
                      AND {end_col} IS NOT NULL
                      AND {start_col} > {end_col};
                """
                
                try:
                    df = pd.read_sql_query(query, self.connection)
                    invalid_count = int(df['invalid_ranges'].iloc[0])
                    
                    status = 'passed' if invalid_count == 0 else 'failed'
                    severity = 'error' if invalid_count > 0 else 'info'
                    
                    checks.append({
                        'check_name': f'date_range_consistency_{start_col}_{end_col}',
                        'invalid_count': invalid_count,
                        'status': status,
                        'severity': severity,
                        'message': f"Found {invalid_count} records where {start_col} > {end_col}" if invalid_count > 0 else f"Date ranges are consistent"
                    })
                except Exception as e:
                    checks.append({
                        'check_name': f'date_range_consistency_{start_col}_{end_col}',
                        'status': 'error',
                        'severity': 'error',
                        'message': f"Error checking date ranges: {str(e)}"
                    })
        
        # Check numeric ranges
        numeric_ranges = table_rules.get('numeric_ranges', [])
        for num_range in numeric_ranges:
            col = num_range.get('column')
            min_val = num_range.get('min')
            max_val = num_range.get('max')
            
            if col and min_val is not None and max_val is not None:
                query = f"""
                    SELECT COUNT(*) as out_of_range
                    FROM {table_name}
                    WHERE {col} < {min_val} OR {col} > {max_val};
                """
                
                try:
                    df = pd.read_sql_query(query, self.connection)
                    out_of_range = int(df['out_of_range'].iloc[0])
                    
                    status = 'passed' if out_of_range == 0 else 'failed'
                    severity = 'warning' if out_of_range > 0 else 'info'
                    
                    checks.append({
                        'check_name': f'numeric_range_{col}',
                        'column': col,
                        'out_of_range_count': out_of_range,
                        'expected_range': f"{min_val} - {max_val}",
                        'status': status,
                        'severity': severity,
                        'message': f"Found {out_of_range} values outside range [{min_val}, {max_val}]" if out_of_range > 0 else f"All values within expected range"
                    })
                except Exception as e:
                    checks.append({
                        'check_name': f'numeric_range_{col}',
                        'column': col,
                        'status': 'error',
                        'severity': 'error',
                        'message': f"Error checking numeric range: {str(e)}"
                    })
        
        # Check enum/categorical values
        categorical_columns = table_rules.get('categorical_columns', [])
        for cat_col in categorical_columns:
            col_name = cat_col.get('name')
            expected_values = cat_col.get('expected_values', [])
            
            if col_name and expected_values:
                # Get actual values
                query = f"""
                    SELECT DISTINCT {col_name} as value, COUNT(*) as count
                    FROM {table_name}
                    WHERE {col_name} IS NOT NULL
                    GROUP BY {col_name}
                    ORDER BY count DESC;
                """
                
                try:
                    df = pd.read_sql_query(query, self.connection)
                    actual_values = set(df['value'].str.lower().str.strip())
                    expected_set = set(str(v).lower().strip() for v in expected_values)
                    
                    unexpected = actual_values - expected_set
                    unexpected_count = len(unexpected)
                    
                    status = 'passed' if unexpected_count == 0 else 'failed'
                    severity = 'warning' if unexpected_count > 0 else 'info'
                    
                    checks.append({
                        'check_name': f'enum_consistency_{col_name}',
                        'column': col_name,
                        'unexpected_values': list(unexpected),
                        'unexpected_count': unexpected_count,
                        'status': status,
                        'severity': severity,
                        'message': f"Found {unexpected_count} unexpected values: {list(unexpected)}" if unexpected_count > 0 else f"All values match expected enum"
                    })
                except Exception as e:
                    checks.append({
                        'check_name': f'enum_consistency_{col_name}',
                        'column': col_name,
                        'status': 'error',
                        'severity': 'error',
                        'message': f"Error checking enum values: {str(e)}"
                    })
        
        return checks
    
    def _check_completeness(self, table_name: str, table_rules: Dict) -> List[Dict[str, Any]]:
        """Check data completeness"""
        checks = []
        
        required_columns = table_rules.get('required_columns', [])
        
        for col in required_columns:
            query = f"""
                SELECT 
                    COUNT(*) as total_rows,
                    COUNT({col}) as non_null_count,
                    ROUND(100.0 * COUNT({col}) / COUNT(*), 2) as completeness_pct
                FROM {table_name};
            """
            
            try:
                df = pd.read_sql_query(query, self.connection)
                completeness = float(df['completeness_pct'].iloc[0])
                non_null = int(df['non_null_count'].iloc[0])
                total = int(df['total_rows'].iloc[0])
                
                threshold = 95  # Default threshold
                status = 'passed' if completeness >= threshold else 'failed'
                severity = 'warning' if completeness < threshold else 'info'
                
                checks.append({
                    'check_name': f'completeness_{col}',
                    'column': col,
                    'completeness_percentage': completeness,
                    'non_null_count': non_null,
                    'total_rows': total,
                    'threshold': threshold,
                    'status': status,
                    'severity': severity,
                    'message': f"Column '{col}' is {completeness:.1f}% complete (threshold: {threshold}%)"
                })
            except Exception as e:
                checks.append({
                    'check_name': f'completeness_{col}',
                    'column': col,
                    'status': 'error',
                    'severity': 'error',
                    'message': f"Error checking completeness: {str(e)}"
                })
        
        return checks
    
    def print_sanity_check_results(self, results: Dict[str, Any]):
        """Print formatted sanity check results"""
        print(f"\n{'='*80}")
        print(f"SANITY CHECKS: {results['table_name']}")
        print(f"{'='*80}")
        
        summary = results['summary']
        print(f"\n📊 Summary:")
        print(f"   Total checks: {summary['total_checks']}")
        print(f"   ✓ Passed: {summary['passed']}")
        print(f"   ⚠️  Warnings: {summary['warnings']}")
        print(f"   ✗ Errors: {summary['errors']}")
        
        # Print null checks
        if results['null_checks']:
            print(f"\n🔍 Null Checks:")
            for check in results['null_checks']:
                status_icon = "✓" if check['status'] == 'passed' else "✗"
                print(f"   {status_icon} {check['message']}")
        
        # Print duplicate checks
        if results['duplicate_checks']:
            print(f"\n🔍 Duplicate Checks:")
            for check in results['duplicate_checks']:
                status_icon = "✓" if check['status'] == 'passed' else "✗"
                print(f"   {status_icon} {check['message']}")
        
        # Print consistency checks
        if results['consistency_checks']:
            print(f"\n🔍 Consistency Checks:")
            for check in results['consistency_checks']:
                status_icon = "✓" if check['status'] == 'passed' else "✗"
                print(f"   {status_icon} {check['message']}")
        
        # Print completeness checks
        if results['completeness_checks']:
            print(f"\n🔍 Completeness Checks:")
            for check in results['completeness_checks']:
                status_icon = "✓" if check['status'] == 'passed' else "✗"
                print(f"   {status_icon} {check['message']}")
        
        print(f"\n{'='*80}\n")


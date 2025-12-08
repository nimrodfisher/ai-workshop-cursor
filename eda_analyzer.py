"""
EDA (Exploratory Data Analysis) Module
Performs EDA based on eda_rules.yml
"""

import yaml
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import psycopg
from datetime import datetime
from scipy import stats


class EDAAnalyzer:
    """
    Performs Exploratory Data Analysis on tables
    """
    
    def __init__(self, connection, rules_file: str = "eda_rules.yml"):
        self.connection = connection
        self.rules = self._load_rules(rules_file)
        self.eda_results: List[Dict[str, Any]] = []
        
    def _load_rules(self, rules_file: str) -> Dict[str, Any]:
        """Load EDA rules from YAML file"""
        try:
            with open(rules_file, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Warning: {rules_file} not found. Using default rules.")
            return {}
        except Exception as e:
            print(f"Error loading rules: {e}")
            return {}
    
    def run_eda(self, table_name: str, sample_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Run EDA on a table
        
        Args:
            table_name: Name of the table to analyze
            sample_size: Optional sample size for large tables
        
        Returns:
            Dictionary with EDA results
        """
        results = {
            'table_name': table_name,
            'timestamp': datetime.now().isoformat(),
            'basic_stats': {},
            'distribution_analysis': {},
            'relationship_analysis': {},
            'time_series_analysis': {},
            'flags': [],
            'typical_questions': []
        }
        
        # Get table data
        limit_clause = f"LIMIT {sample_size}" if sample_size else ""
        query = f"SELECT * FROM {table_name} {limit_clause};"
        df = pd.read_sql_query(query, self.connection)
        
        if df.empty:
            return results
        
        # Run basic stats
        if self.rules.get('eda_phases', {}).get('basic_stats', {}).get('enabled', True):
            results['basic_stats'] = self._calculate_basic_stats(df, table_name)
        
        # Run distribution analysis
        if self.rules.get('eda_phases', {}).get('distribution_analysis', {}).get('enabled', True):
            results['distribution_analysis'] = self._analyze_distributions(df)
        
        # Run relationship analysis
        if self.rules.get('eda_phases', {}).get('relationship_analysis', {}).get('enabled', True):
            results['relationship_analysis'] = self._analyze_relationships(df)
        
        # Check if time-series
        date_columns = [col for col in df.columns if any(date_word in col.lower() for date_word in ['date', 'time', 'created', 'occurred', 'timestamp'])]
        if date_columns and self.rules.get('eda_phases', {}).get('time_series_analysis', {}).get('enabled', True):
            results['time_series_analysis'] = self._analyze_time_series(df, date_columns[0])
        
        # Generate flags and typical questions
        results['flags'] = self._generate_flags(results)
        results['typical_questions'] = self._generate_typical_questions(results)
        
        self.eda_results.append(results)
        return results
    
    def _calculate_basic_stats(self, df: pd.DataFrame, table_name: str) -> Dict[str, Any]:
        """Calculate basic descriptive statistics"""
        stats_dict = {
            'row_count': len(df),
            'column_count': len(df.columns),
            'columns': list(df.columns),
            'numeric_summary': {},
            'categorical_summary': {},
            'null_summary': {}
        }
        
        # Null summary
        null_counts = df.isnull().sum()
        null_pct = (null_counts / len(df)) * 100
        stats_dict['null_summary'] = {
            col: {
                'null_count': int(null_counts[col]),
                'null_percentage': float(null_pct[col])
            }
            for col in df.columns
            if null_counts[col] > 0
        }
        
        # Numeric summary
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            stats_dict['numeric_summary'][col] = {
                'count': int(df[col].count()),
                'mean': float(df[col].mean()) if not df[col].isna().all() else None,
                'median': float(df[col].median()) if not df[col].isna().all() else None,
                'std': float(df[col].std()) if not df[col].isna().all() else None,
                'min': float(df[col].min()) if not df[col].isna().all() else None,
                'max': float(df[col].max()) if not df[col].isna().all() else None,
                'q25': float(df[col].quantile(0.25)) if not df[col].isna().all() else None,
                'q75': float(df[col].quantile(0.75)) if not df[col].isna().all() else None
            }
        
        # Categorical summary
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            value_counts = df[col].value_counts().head(10)
            stats_dict['categorical_summary'][col] = {
                'unique_count': int(df[col].nunique()),
                'top_values': value_counts.to_dict(),
                'null_count': int(df[col].isnull().sum())
            }
        
        # Date range
        date_cols = [col for col in df.columns if any(word in col.lower() for word in ['date', 'time', 'created', 'occurred', 'timestamp'])]
        for col in date_cols:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                if df[col].notna().any():
                    stats_dict['date_range'] = {
                        col: {
                            'min': str(df[col].min()),
                            'max': str(df[col].max()),
                            'span_days': (df[col].max() - df[col].min()).days if df[col].notna().any() else None
                        }
                    }
            except:
                pass
        
        return stats_dict
    
    def _analyze_distributions(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze data distributions"""
        distribution_info = {
            'numeric_distributions': {},
            'categorical_distributions': {},
            'flags': []
        }
        
        # Numeric distributions
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].notna().sum() == 0:
                continue
                
            col_data = df[col].dropna()
            if len(col_data) == 0:
                continue
            
            # Calculate skewness
            skewness = float(stats.skew(col_data))
            
            # Calculate outliers (IQR method)
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
            
            # Zero inflation
            zero_count = (col_data == 0).sum()
            zero_pct = (zero_count / len(col_data)) * 100
            
            distribution_info['numeric_distributions'][col] = {
                'skewness': skewness,
                'outlier_count': int(len(outliers)),
                'outlier_percentage': float((len(outliers) / len(col_data)) * 100),
                'zero_count': int(zero_count),
                'zero_percentage': float(zero_pct)
            }
            
            # Generate flags
            if abs(skewness) > 2:
                distribution_info['flags'].append({
                    'type': 'high_skewness',
                    'column': col,
                    'value': skewness,
                    'message': f"Highly skewed distribution detected in '{col}' (skewness: {skewness:.2f})"
                })
            
            if len(outliers) > 0:
                distribution_info['flags'].append({
                    'type': 'outliers',
                    'column': col,
                    'count': int(len(outliers)),
                    'message': f"Potential outliers detected in '{col}' ({len(outliers)} values)"
                })
            
            if zero_pct > 50:
                distribution_info['flags'].append({
                    'type': 'zero_inflation',
                    'column': col,
                    'percentage': float(zero_pct),
                    'message': f"High percentage of zero values in '{col}' ({zero_pct:.1f}%)"
                })
        
        # Categorical distributions
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            unique_count = df[col].nunique()
            total_count = df[col].count()
            value_counts = df[col].value_counts()
            max_class_pct = (value_counts.iloc[0] / total_count * 100) if total_count > 0 else 0
            
            distribution_info['categorical_distributions'][col] = {
                'unique_count': int(unique_count),
                'max_class_percentage': float(max_class_pct),
                'top_value': value_counts.index[0] if len(value_counts) > 0 else None
            }
            
            # Generate flags
            if unique_count > 50:
                distribution_info['flags'].append({
                    'type': 'high_cardinality',
                    'column': col,
                    'unique_count': int(unique_count),
                    'message': f"High cardinality in '{col}' ({unique_count} unique values) - consider grouping"
                })
            
            if max_class_pct > 90:
                distribution_info['flags'].append({
                    'type': 'imbalanced_classes',
                    'column': col,
                    'percentage': float(max_class_pct),
                    'message': f"Highly imbalanced classes in '{col}' (top class: {max_class_pct:.1f}%)"
                })
        
        return distribution_info
    
    def _analyze_relationships(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze relationships between columns"""
        relationship_info = {
            'correlations': {},
            'flags': []
        }
        
        # Calculate correlations for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            
            # Find high correlations
            for i, col1 in enumerate(numeric_cols):
                for col2 in numeric_cols[i+1:]:
                    corr_value = corr_matrix.loc[col1, col2]
                    if not np.isnan(corr_value):
                        relationship_info['correlations'][f"{col1}_{col2}"] = {
                            'column1': col1,
                            'column2': col2,
                            'correlation': float(corr_value)
                        }
                        
                        if abs(corr_value) > 0.7:
                            relationship_info['flags'].append({
                                'type': 'high_correlation',
                                'columns': [col1, col2],
                                'correlation': float(corr_value),
                                'message': f"High correlation between '{col1}' and '{col2}' ({corr_value:.2f})"
                            })
        
        return relationship_info
    
    def _analyze_time_series(self, df: pd.DataFrame, date_column: str) -> Dict[str, Any]:
        """Analyze time-series patterns"""
        ts_info = {
            'temporal_coverage': {},
            'flags': []
        }
        
        try:
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
            df_sorted = df.sort_values(date_column)
            
            if df_sorted[date_column].notna().any():
                # Check for gaps
                date_diff = df_sorted[date_column].diff()
                max_gap_days = date_diff.max().days if hasattr(date_diff.max(), 'days') else 0
                
                # Check recent data
                last_date = df_sorted[date_column].max()
                days_since_last = (datetime.now() - last_date).days if isinstance(last_date, datetime) else None
                
                ts_info['temporal_coverage'] = {
                    'first_date': str(df_sorted[date_column].min()),
                    'last_date': str(last_date),
                    'max_gap_days': int(max_gap_days),
                    'days_since_last': int(days_since_last) if days_since_last else None
                }
                
                # Generate flags
                if max_gap_days > 7:
                    ts_info['flags'].append({
                        'type': 'data_gaps',
                        'max_gap_days': int(max_gap_days),
                        'message': f"Gaps of more than 7 days detected (max gap: {max_gap_days} days)"
                    })
                
                if days_since_last and days_since_last > 7:
                    ts_info['flags'].append({
                        'type': 'recent_data_missing',
                        'days_since_last': int(days_since_last),
                        'message': f"No recent data (last record: {days_since_last} days ago)"
                    })
        except Exception as e:
            ts_info['error'] = str(e)
        
        return ts_info
    
    def _generate_flags(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate flags from EDA results"""
        flags = []
        
        # Collect flags from distribution analysis
        if 'distribution_analysis' in results and 'flags' in results['distribution_analysis']:
            flags.extend(results['distribution_analysis']['flags'])
        
        # Collect flags from relationship analysis
        if 'relationship_analysis' in results and 'flags' in results['relationship_analysis']:
            flags.extend(results['relationship_analysis']['flags'])
        
        # Collect flags from time series analysis
        if 'time_series_analysis' in results and 'flags' in results['time_series_analysis']:
            flags.extend(results['time_series_analysis']['flags'])
        
        return flags
    
    def _generate_typical_questions(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate typical questions based on EDA results"""
        questions = []
        typical_qs = self.rules.get('typical_questions', [])
        
        # Check null percentages
        if 'basic_stats' in results and 'null_summary' in results['basic_stats']:
            for col, null_info in results['basic_stats']['null_summary'].items():
                if null_info['null_percentage'] > 30:
                    questions.append({
                        'question': f"Why are there so many null values in column '{col}'?",
                        'trigger': f"null_percentage > 30",
                        'explanation': f"Column '{col}' has {null_info['null_percentage']:.1f}% null values"
                    })
        
        # Check for outliers
        if 'distribution_analysis' in results:
            for flag in results['distribution_analysis'].get('flags', []):
                if flag['type'] == 'outliers':
                    questions.append({
                        'question': f"Are there outliers in '{flag['column']}'?",
                        'trigger': 'outliers_detected',
                        'explanation': flag['message']
                    })
        
        # Check for high correlation
        if 'relationship_analysis' in results:
            for flag in results['relationship_analysis'].get('flags', []):
                if flag['type'] == 'high_correlation':
                    questions.append({
                        'question': f"Why is there high correlation between '{flag['columns'][0]}' and '{flag['columns'][1]}'?",
                        'trigger': 'high_correlation_detected',
                        'explanation': flag['message']
                    })
        
        return questions
    
    def print_eda_results(self, results: Dict[str, Any]):
        """Print formatted EDA results"""
        print(f"\n{'='*80}")
        print(f"EXPLORATORY DATA ANALYSIS: {results['table_name']}")
        print(f"{'='*80}")
        
        # Basic stats
        if 'basic_stats' in results:
            bs = results['basic_stats']
            print(f"\n📊 Basic Statistics:")
            print(f"   Rows: {bs.get('row_count', 'N/A'):,}")
            print(f"   Columns: {bs.get('column_count', 'N/A')}")
            
            if 'null_summary' in bs and bs['null_summary']:
                print(f"\n   Null Values:")
                for col, null_info in list(bs['null_summary'].items())[:5]:
                    print(f"      • {col}: {null_info['null_count']} ({null_info['null_percentage']:.1f}%)")
            
            if 'numeric_summary' in bs and bs['numeric_summary']:
                print(f"\n   Numeric Columns Summary:")
                for col, stats in list(bs['numeric_summary'].items())[:3]:
                    if stats.get('mean') is not None:
                        print(f"      • {col}:")
                        print(f"        Mean: {stats['mean']:.2f}, Median: {stats['median']:.2f}")
                        print(f"        Min: {stats['min']:.2f}, Max: {stats['max']:.2f}")
        
        # Flags
        if results.get('flags'):
            print(f"\n🚩 Flags Raised:")
            for flag in results['flags'][:10]:
                print(f"   ⚠️  {flag.get('message', 'N/A')}")
        
        # Typical questions
        if results.get('typical_questions'):
            print(f"\n❓ Typical Questions:")
            for q in results['typical_questions'][:5]:
                print(f"   • {q.get('question', 'N/A')}")
                print(f"     {q.get('explanation', '')}")
        
        print(f"\n{'='*80}\n")


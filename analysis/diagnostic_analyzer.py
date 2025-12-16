"""
Diagnostic Analyzer and Segment Comparison Module
Performs diagnostic analysis and compares segments
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from scipy import stats


class DiagnosticAnalyzer:
    """
    Performs diagnostic analysis and segment comparisons
    """
    
    def __init__(self):
        self.diagnostic_results: List[Dict[str, Any]] = []
    
    def compare_segments(
        self,
        df: pd.DataFrame,
        segment_column: str,
        metric_column: str,
        segments: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Compare segments on a metric
        
        Args:
            df: DataFrame with data
            segment_column: Column defining segments
            metric_column: Column with metric to compare
            segments: Optional list of specific segments to compare
        
        Returns:
            Comparison results
        """
        if segment_column not in df.columns or metric_column not in df.columns:
            return {'error': 'Columns not found'}
        
        # Filter segments if specified
        if segments:
            df_filtered = df[df[segment_column].isin(segments)]
        else:
            df_filtered = df
        
        # Get unique segments
        unique_segments = df_filtered[segment_column].dropna().unique()
        
        comparison = {
            'segment_column': segment_column,
            'metric_column': metric_column,
            'segments_compared': list(unique_segments),
            'segment_stats': {},
            'comparisons': {},
            'significance_tests': {}
        }
        
        # Calculate stats for each segment
        for segment in unique_segments:
            segment_data = df_filtered[df_filtered[segment_column] == segment][metric_column].dropna()
            
            if len(segment_data) > 0:
                comparison['segment_stats'][segment] = {
                    'count': int(len(segment_data)),
                    'mean': float(segment_data.mean()),
                    'median': float(segment_data.median()),
                    'std': float(segment_data.std()),
                    'min': float(segment_data.min()),
                    'max': float(segment_data.max()),
                    'q25': float(segment_data.quantile(0.25)),
                    'q75': float(segment_data.quantile(0.75))
                }
        
        # Compare segments pairwise
        segments_list = list(unique_segments)
        for i, seg1 in enumerate(segments_list):
            for seg2 in segments_list[i+1:]:
                seg1_data = df_filtered[df_filtered[segment_column] == seg1][metric_column].dropna()
                seg2_data = df_filtered[df_filtered[segment_column] == seg2][metric_column].dropna()
                
                if len(seg1_data) > 0 and len(seg2_data) > 0:
                    # Statistical test (t-test for means)
                    try:
                        t_stat, p_value = stats.ttest_ind(seg1_data, seg2_data)
                        
                        comparison['comparisons'][f"{seg1}_vs_{seg2}"] = {
                            'mean_diff': float(seg1_data.mean() - seg2_data.mean()),
                            'mean_diff_pct': float(((seg1_data.mean() - seg2_data.mean()) / seg2_data.mean() * 100) if seg2_data.mean() != 0 else 0),
                            't_statistic': float(t_stat),
                            'p_value': float(p_value),
                            'significant': p_value < 0.05
                        }
                    except:
                        pass
        
        return comparison
    
    def diagnostic_analysis(
        self,
        df: pd.DataFrame,
        target_column: str,
        segment_columns: List[str],
        diagnostic_type: str = "performance"
    ) -> Dict[str, Any]:
        """
        Perform diagnostic analysis
        
        Args:
            df: DataFrame with data
            target_column: Column to analyze (target metric)
            segment_columns: Columns to segment by
            diagnostic_type: Type of diagnostic (performance, quality, etc.)
        
        Returns:
            Diagnostic results
        """
        diagnostics = {
            'target_column': target_column,
            'segment_columns': segment_columns,
            'diagnostic_type': diagnostic_type,
            'segment_comparisons': {},
            'insights': []
        }
        
        # Compare segments
        for seg_col in segment_columns:
            if seg_col in df.columns:
                comparison = self.compare_segments(df, seg_col, target_column)
                diagnostics['segment_comparisons'][seg_col] = comparison
                
                # Generate insights
                insights = self._generate_insights(comparison, seg_col, target_column)
                diagnostics['insights'].extend(insights)
        
        return diagnostics
    
    def _generate_insights(
        self,
        comparison: Dict[str, Any],
        segment_column: str,
        metric_column: str
    ) -> List[Dict[str, Any]]:
        """Generate insights from segment comparison"""
        insights = []
        
        segment_stats = comparison.get('segment_stats', {})
        if len(segment_stats) < 2:
            return insights
        
        # Find best and worst performing segments
        means = {seg: stats['mean'] for seg, stats in segment_stats.items()}
        if means:
            best_segment = max(means, key=means.get)
            worst_segment = min(means, key=means.get)
            
            best_mean = means[best_segment]
            worst_mean = means[worst_segment]
            diff_pct = ((best_mean - worst_mean) / worst_mean * 100) if worst_mean != 0 else 0
            
            insights.append({
                'type': 'performance_gap',
                'message': f"'{best_segment}' performs {diff_pct:.1f}% better than '{worst_segment}' on {metric_column}",
                'best_segment': best_segment,
                'worst_segment': worst_segment,
                'difference_pct': float(diff_pct)
            })
        
        # Check for significant differences
        comparisons = comparison.get('comparisons', {})
        for comp_name, comp_data in comparisons.items():
            if comp_data.get('significant'):
                insights.append({
                    'type': 'significant_difference',
                    'message': f"Statistically significant difference found: {comp_name} (p={comp_data['p_value']:.4f})",
                    'comparison': comp_name,
                    'p_value': comp_data['p_value']
                })
        
        return insights
    
    def print_diagnostic_results(self, results: Dict[str, Any]):
        """Print formatted diagnostic results"""
        print(f"\n{'='*80}")
        print(f"DIAGNOSTIC ANALYSIS")
        print(f"{'='*80}")
        
        print(f"\n📊 Target Metric: {results.get('target_column', 'N/A')}")
        print(f"📊 Segments: {', '.join(results.get('segment_columns', []))}")
        
        # Segment comparisons
        if 'segment_comparisons' in results:
            for seg_col, comparison in results['segment_comparisons'].items():
                print(f"\n🔍 Segment Comparison: {seg_col}")
                
                segment_stats = comparison.get('segment_stats', {})
                for segment, stats in segment_stats.items():
                    print(f"   • {segment}:")
                    print(f"     Mean: {stats['mean']:.2f}, Median: {stats['median']:.2f}")
                    print(f"     Count: {stats['count']}")
                
                # Show comparisons
                comparisons = comparison.get('comparisons', {})
                if comparisons:
                    print(f"\n   Comparisons:")
                    for comp_name, comp_data in list(comparisons.items())[:3]:
                        sig = "✓" if comp_data.get('significant') else "✗"
                        print(f"     {sig} {comp_name}: {comp_data['mean_diff_pct']:.1f}% difference (p={comp_data['p_value']:.4f})")
        
        # Insights
        if results.get('insights'):
            print(f"\n💡 Insights:")
            for insight in results['insights'][:5]:
                print(f"   • {insight.get('message', 'N/A')}")
        
        print(f"\n{'='*80}\n")


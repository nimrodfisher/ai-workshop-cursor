"""
Calculate Engagement Weights for Scoring Model
Based on correlation analysis with Churn status
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

def load_data(file_path):
    """Load the CSV file into a pandas DataFrame"""
    print("="*80)
    print("LOADING DATA")
    print("="*80)
    df = pd.read_csv(file_path)
    print(f"✓ Data loaded successfully!")
    print(f"  Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df

def calculate_correlations(df):
    """Calculate correlation between numerical activity columns and Churned status"""
    print("\n" + "="*80)
    print("CORRELATION ANALYSIS")
    print("="*80)
    
    # Select numerical activity columns (exclude User_ID and Subscription_Tier)
    activity_columns = [
        'Num_Logins', 'Num_Searches', 'Num_Card_Views', 
        'Num_API_Calls', 'Num_Exports', 'Num_Emails_Sent'
    ]
    
    # Calculate correlation with Churned
    correlations = {}
    for col in activity_columns:
        corr = df[col].corr(df['Churned'])
        correlations[col] = corr
        print(f"  {col:20s}: {corr:7.4f}")
    
    return correlations, activity_columns

def calculate_weights(correlations):
    """
    Calculate engagement weights:
    1. Invert correlation (multiply by -1) - negative corr with Churn = positive impact on Retention
    2. Normalize to 1-10 scale (10 = most impactful)
    """
    print("\n" + "="*80)
    print("CALCULATING ENGAGEMENT WEIGHTS")
    print("="*80)
    
    # Step 1: Invert correlations (multiply by -1)
    inverted_correlations = {k: -v for k, v in correlations.items()}
    print("\n1. Inverted Correlations (negative corr with Churn = positive impact on Retention):")
    for col, val in inverted_correlations.items():
        print(f"   {col:20s}: {val:7.4f}")
    
    # Step 2: Normalize to 1-10 scale
    # Formula: weight = 1 + (value - min) / (max - min) * 9
    values = list(inverted_correlations.values())
    min_val = min(values)
    max_val = max(values)
    
    print(f"\n2. Normalization parameters:")
    print(f"   Min inverted correlation: {min_val:.4f}")
    print(f"   Max inverted correlation: {max_val:.4f}")
    print(f"   Range: {max_val - min_val:.4f}")
    
    weights = {}
    for col, val in inverted_correlations.items():
        # Normalize to 1-10 scale
        if max_val == min_val:
            # Edge case: all values are the same
            weight = 5.5  # Middle of 1-10 scale
        else:
            weight = 1 + (val - min_val) / (max_val - min_val) * 9
        weights[col] = round(weight, 2)
        print(f"   {col:20s}: {weight:6.2f}")
    
    return weights, inverted_correlations

def plot_correlation_heatmap(df, activity_columns):
    """Plot correlation heatmap for all numerical columns"""
    print("\n" + "="*80)
    print("GENERATING CORRELATION HEATMAP")
    print("="*80)
    
    # Select numerical columns for correlation matrix
    numerical_cols = activity_columns + ['Churned']
    corr_matrix = df[numerical_cols].corr()
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create custom colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    
    # Generate heatmap
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap=cmap, 
                center=0, square=True, linewidths=1, 
                cbar_kws={"shrink": 0.8}, ax=ax,
                vmin=-1, vmax=1)
    
    ax.set_title('Correlation Heatmap: Activity Metrics vs Churn Status', 
                 fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: correlation_heatmap.png")
    plt.close()

def plot_engagement_weights(weights):
    """Plot bar chart showing AI-Recommended Weights"""
    print("\n" + "="*80)
    print("GENERATING ENGAGEMENT WEIGHTS BAR CHART")
    print("="*80)
    
    # Sort weights by value (descending)
    sorted_weights = dict(sorted(weights.items(), key=lambda x: x[1], reverse=True))
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Create color gradient from low to high
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(sorted_weights)))
    
    bars = ax.barh(list(sorted_weights.keys()), list(sorted_weights.values()), 
                   color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for i, (col, weight) in enumerate(sorted_weights.items()):
        ax.text(weight + 0.1, i, f'{weight:.2f}', 
               va='center', fontsize=11, fontweight='bold')
    
    ax.set_xlabel('Engagement Weight (1-10 Scale)', fontsize=13, fontweight='bold')
    ax.set_title('AI-Recommended Engagement Weights for Scoring Model', 
                 fontsize=15, fontweight='bold', pad=20)
    ax.set_xlim(0, 11)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Add vertical line at middle (5.5)
    ax.axvline(x=5.5, color='red', linestyle='--', alpha=0.5, linewidth=1, label='Midpoint (5.5)')
    ax.legend(loc='lower right')
    
    plt.tight_layout()
    plt.savefig('engagement_weights_bar_chart.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: engagement_weights_bar_chart.png")
    plt.close()

def print_weights_dictionary(weights):
    """Print the final weights as a dictionary"""
    print("\n" + "="*80)
    print("FINAL ENGAGEMENT WEIGHTS DICTIONARY")
    print("="*80)
    print("\nweights = {")
    for col, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
        print(f"    '{col}': {weight:.2f},")
    print("}")
    
    # Also print as a Python dictionary string for easy copying
    print("\n" + "-"*80)
    print("Python Dictionary (copy-ready):")
    print("-"*80)
    dict_str = "weights = {\n"
    for col, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
        dict_str += f"    '{col}': {weight:.2f},\n"
    dict_str += "}"
    print(dict_str)

def main():
    """Main execution function"""
    # Load data
    df = load_data('saas_aggregated_data.csv')
    
    # Calculate correlations
    correlations, activity_columns = calculate_correlations(df)
    
    # Calculate weights
    weights, inverted_correlations = calculate_weights(correlations)
    
    # Plot correlation heatmap
    plot_correlation_heatmap(df, activity_columns)
    
    # Plot engagement weights bar chart
    plot_engagement_weights(weights)
    
    # Print weights dictionary
    print_weights_dictionary(weights)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\nGenerated files:")
    print("  - correlation_heatmap.png")
    print("  - engagement_weights_bar_chart.png")
    
    return weights

if __name__ == "__main__":
    weights = main()


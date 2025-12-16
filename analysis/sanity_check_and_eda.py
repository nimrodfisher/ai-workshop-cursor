"""
Data Quality Sanity Check and Exploratory Data Analysis
for B2B SaaS User Activity Dataset
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def load_data(file_path):
    """Load the CSV file into a pandas DataFrame"""
    print("="*80)
    print("LOADING DATA")
    print("="*80)
    df = pd.read_csv(file_path)
    print(f"✓ Data loaded successfully!")
    print(f"  Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df

def sanity_check(df):
    """Perform data quality sanity checks"""
    print("\n" + "="*80)
    print("SANITY CHECK REPORT")
    print("="*80)
    
    results = {}
    
    # 1. Missing Values
    print("\n1. MISSING VALUES CHECK")
    print("-" * 80)
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        'Column': missing.index,
        'Missing Count': missing.values,
        'Missing Percentage': missing_pct.values
    })
    missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
    
    if len(missing_df) == 0:
        print("✓ No missing values found in any column")
        results['missing_values'] = {'status': 'PASS', 'details': 'No missing values'}
    else:
        print("⚠ Missing values detected:")
        print(missing_df.to_string(index=False))
        results['missing_values'] = {'status': 'WARNING', 'details': missing_df.to_dict('records')}
    
    # 2. Duplicates
    print("\n2. DUPLICATE CHECK")
    print("-" * 80)
    total_duplicates = df.duplicated().sum()
    if total_duplicates == 0:
        print("✓ No duplicate rows found")
        results['duplicates'] = {'status': 'PASS', 'count': 0}
    else:
        print(f"⚠ Found {total_duplicates:,} duplicate rows ({total_duplicates/len(df)*100:.2f}%)")
        results['duplicates'] = {'status': 'WARNING', 'count': total_duplicates}
    
    # Check for duplicate User_IDs (business key)
    duplicate_user_ids = df['User_ID'].duplicated().sum()
    if duplicate_user_ids == 0:
        print("✓ No duplicate User_IDs found")
        results['duplicate_user_ids'] = {'status': 'PASS', 'count': 0}
    else:
        print(f"⚠ Found {duplicate_user_ids:,} duplicate User_IDs ({duplicate_user_ids/len(df)*100:.2f}%)")
        results['duplicate_user_ids'] = {'status': 'ERROR', 'count': duplicate_user_ids}
    
    # 3. Data Types
    print("\n3. DATA TYPES CHECK")
    print("-" * 80)
    dtype_info = pd.DataFrame({
        'Column': df.dtypes.index,
        'Data Type': df.dtypes.values,
        'Non-Null Count': df.count().values,
        'Total Count': len(df)
    })
    print(dtype_info.to_string(index=False))
    results['data_types'] = dtype_info.to_dict('records')
    
    # 4. Basic Statistics Summary
    print("\n4. BASIC STATISTICS SUMMARY")
    print("-" * 80)
    print(f"Total Records: {len(df):,}")
    print(f"Total Columns: {len(df.columns)}")
    print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # 5. Target Variable Check
    print("\n5. TARGET VARIABLE (Churned) CHECK")
    print("-" * 80)
    churn_counts = df['Churned'].value_counts().sort_index()
    churn_pct = df['Churned'].value_counts(normalize=True).sort_index() * 100
    print("Churn Distribution:")
    for val in churn_counts.index:
        status = "Retained" if val == 0 else "Churned"
        print(f"  {status} ({val}): {churn_counts[val]:,} users ({churn_pct[val]:.2f}%)")
    results['churn_distribution'] = {
        'retained': int(churn_counts.get(0, 0)),
        'churned': int(churn_counts.get(1, 0)),
        'retention_rate': float(churn_pct.get(0, 0)),
        'churn_rate': float(churn_pct.get(1, 0))
    }
    
    return results

def plot_churn_distribution(df):
    """Plot the distribution of the Churned variable"""
    print("\n" + "="*80)
    print("PLOTTING CHURN DISTRIBUTION")
    print("="*80)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Count plot
    churn_counts = df['Churned'].value_counts().sort_index()
    colors = ['#2ecc71', '#e74c3c']  # Green for retained, red for churned
    labels = ['Retained (0)', 'Churned (1)']
    
    bars = ax1.bar(labels, churn_counts.values, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Number of Users', fontsize=12, fontweight='bold')
    ax1.set_title('Churn Distribution (Count)', fontsize=14, fontweight='bold', pad=20)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}\n({height/len(df)*100:.1f}%)',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Pie chart
    churn_pct = df['Churned'].value_counts(normalize=True).sort_index() * 100
    ax2.pie(churn_counts.values, labels=labels, autopct='%1.1f%%', 
            colors=colors, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax2.set_title('Churn Distribution (Percentage)', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('churn_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: churn_distribution.png")
    plt.show()

def plot_activity_vs_churn(df):
    """Create boxplots comparing activity metrics between Retained and Churned users"""
    print("\n" + "="*80)
    print("PLOTTING ACTIVITY METRICS vs CHURN")
    print("="*80)
    
    metrics = ['Num_Exports', 'Num_Logins', 'Num_API_Calls']
    n_metrics = len(metrics)
    
    fig, axes = plt.subplots(1, n_metrics, figsize=(18, 6))
    
    for idx, metric in enumerate(metrics):
        ax = axes[idx]
        
        # Prepare data for boxplot
        retained = df[df['Churned'] == 0][metric]
        churned = df[df['Churned'] == 1][metric]
        
        # Create boxplot
        box_data = [retained, churned]
        bp = ax.boxplot(box_data, tick_labels=['Retained (0)', 'Churned (1)'], 
                       patch_artist=True, showmeans=True, meanline=True)
        
        # Color the boxes
        colors_box = ['#2ecc71', '#e74c3c']
        for patch, color in zip(bp['boxes'], colors_box):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        # Style the plot
        ax.set_ylabel(metric, fontsize=12, fontweight='bold')
        ax.set_title(f'{metric} by Churn Status', fontsize=13, fontweight='bold', pad=15)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Add summary statistics
        retained_median = retained.median()
        churned_median = churned.median()
        retained_mean = retained.mean()
        churned_mean = churned.mean()
        
        stats_text = f'Retained:\n  Median: {retained_median:.1f}\n  Mean: {retained_mean:.1f}\n\n'
        stats_text += f'Churned:\n  Median: {churned_median:.1f}\n  Mean: {churned_mean:.1f}'
        
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
               fontsize=9, verticalalignment='top', 
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('activity_vs_churn_boxplots.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: activity_vs_churn_boxplots.png")
    plt.show()

def main():
    """Main execution function"""
    # Load data
    df = load_data('saas_aggregated_data.csv')
    
    # Display head of dataframe
    print("\n" + "="*80)
    print("DATA PREVIEW (First 10 rows)")
    print("="*80)
    print(df.head(10).to_string())
    
    # Sanity check
    sanity_results = sanity_check(df)
    
    # Plot churn distribution
    plot_churn_distribution(df)
    
    # Plot activity vs churn
    plot_activity_vs_churn(df)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\nGenerated files:")
    print("  - churn_distribution.png")
    print("  - activity_vs_churn_boxplots.png")

if __name__ == "__main__":
    main()


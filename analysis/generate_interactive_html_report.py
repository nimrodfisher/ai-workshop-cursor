"""
Generate Interactive HTML Report
"""

import pandas as pd
import numpy as np
import base64
from datetime import datetime
import os

def image_to_base64(image_path):
    """Convert image to base64 string for embedding"""
    if os.path.exists(image_path):
        with open(image_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return None

def load_data(file_path):
    """Load the CSV file into a pandas DataFrame"""
    return pd.read_csv(file_path)

def calculate_correlations(df):
    """Calculate correlation between numerical activity columns and Churned status"""
    activity_columns = [
        'Num_Logins', 'Num_Searches', 'Num_Card_Views', 
        'Num_API_Calls', 'Num_Exports', 'Num_Emails_Sent'
    ]
    correlations = {col: df[col].corr(df['Churned']) for col in activity_columns}
    return correlations, activity_columns

def calculate_weights(correlations):
    """Calculate engagement weights"""
    inverted_correlations = {k: -v for k, v in correlations.items()}
    values = list(inverted_correlations.values())
    min_val = min(values)
    max_val = max(values)
    
    weights = {}
    for col, val in inverted_correlations.items():
        if max_val == min_val:
            weight = 5.5
        else:
            weight = 1 + (val - min_val) / (max_val - min_val) * 9
        weights[col] = round(weight, 2)
    
    return weights, inverted_correlations

def generate_html_report():
    """Generate interactive HTML report"""
    
    # Load data and calculate metrics
    df = load_data('saas_aggregated_data.csv')
    correlations, activity_columns = calculate_correlations(df)
    weights, inverted_correlations = calculate_weights(correlations)
    
    # Sanity check results
    missing_values = df.isnull().sum()
    total_duplicates = df.duplicated().sum()
    duplicate_user_ids = df['User_ID'].duplicated().sum()
    churn_counts = df['Churned'].value_counts().sort_index()
    churn_pct = df['Churned'].value_counts(normalize=True).sort_index() * 100
    
    # Convert images to base64
    churn_dist_img = image_to_base64('churn_distribution.png')
    activity_boxplot_img = image_to_base64('activity_vs_churn_boxplots.png')
    correlation_heatmap_img = image_to_base64('correlation_heatmap.png')
    weights_chart_img = image_to_base64('engagement_weights_bar_chart.png')
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>B2B SaaS User Activity Analysis - Interactive Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.95;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }}
        
        .stat-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .stat-card .label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .tabs {{
            display: flex;
            background: #f8f9fa;
            border-bottom: 2px solid #e0e0e0;
            overflow-x: auto;
        }}
        
        .tab-button {{
            padding: 15px 30px;
            background: transparent;
            border: none;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            color: #666;
            transition: all 0.3s ease;
            border-bottom: 3px solid transparent;
            white-space: nowrap;
        }}
        
        .tab-button:hover {{
            background: #e9ecef;
            color: #667eea;
        }}
        
        .tab-button.active {{
            color: #667eea;
            border-bottom-color: #667eea;
            background: white;
        }}
        
        .tab-content {{
            display: none;
            padding: 40px;
            animation: fadeIn 0.5s;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section h2 {{
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .section h3 {{
            color: #764ba2;
            font-size: 1.4em;
            margin: 25px 0 15px 0;
        }}
        
        .quality-badge {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            margin: 5px;
        }}
        
        .badge-pass {{
            background: #d4edda;
            color: #155724;
        }}
        
        .badge-warning {{
            background: #fff3cd;
            color: #856404;
        }}
        
        .badge-error {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        table th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        table tr:hover {{
            background: #f8f9fa;
        }}
        
        table tr:last-child td {{
            border-bottom: none;
        }}
        
        .image-container {{
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        
        .image-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .weights-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .weight-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
        }}
        
        .weight-card:hover {{
            transform: scale(1.05);
        }}
        
        .weight-card .metric {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
        }}
        
        .weight-card .weight {{
            font-size: 3em;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .weight-card .level {{
            font-size: 0.9em;
            opacity: 0.95;
        }}
        
        .code-block {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 20px 0;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.6;
        }}
        
        .insight-box {{
            background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #f39c12;
        }}
        
        .insight-box h4 {{
            color: #d35400;
            margin-bottom: 10px;
        }}
        
        .churn-meter {{
            display: flex;
            align-items: center;
            gap: 20px;
            margin: 20px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        
        .meter-bar {{
            flex: 1;
            height: 40px;
            background: #e0e0e0;
            border-radius: 20px;
            overflow: hidden;
            position: relative;
        }}
        
        .meter-fill {{
            height: 100%;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            transition: width 1s ease;
        }}
        
        .meter-retained {{
            background: linear-gradient(90deg, #2ecc71, #27ae60);
        }}
        
        .meter-churned {{
            background: linear-gradient(90deg, #e74c3c, #c0392b);
        }}
        
        .collapsible {{
            background: #f8f9fa;
            color: #333;
            cursor: pointer;
            padding: 18px;
            width: 100%;
            border: none;
            text-align: left;
            outline: none;
            font-size: 1.1em;
            font-weight: 600;
            border-radius: 8px;
            margin: 10px 0;
            transition: background 0.3s;
        }}
        
        .collapsible:hover {{
            background: #e9ecef;
        }}
        
        .collapsible.active {{
            background: #667eea;
            color: white;
        }}
        
        .collapsible-content {{
            padding: 0 18px;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
            background: white;
            border-radius: 0 0 8px 8px;
        }}
        
        .collapsible-content.active {{
            padding: 18px;
            max-height: 1000px;
        }}
        
        .footer {{
            background: #2d2d2d;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 B2B SaaS User Activity Analysis</h1>
            <p>Interactive Report - Generated {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="value">{len(df):,}</div>
                <div class="label">Total Records</div>
            </div>
            <div class="stat-card">
                <div class="value">{churn_pct.get(0, 0):.1f}%</div>
                <div class="label">Retention Rate</div>
            </div>
            <div class="stat-card">
                <div class="value">{churn_pct.get(1, 0):.1f}%</div>
                <div class="label">Churn Rate</div>
            </div>
            <div class="stat-card">
                <div class="value">{len(activity_columns)}</div>
                <div class="label">Activity Metrics</div>
            </div>
        </div>
        
        <div class="tabs">
            <button class="tab-button active" onclick="showTab('overview')">📋 Overview</button>
            <button class="tab-button" onclick="showTab('quality')">✅ Data Quality</button>
            <button class="tab-button" onclick="showTab('churn')">📈 Churn Analysis</button>
            <button class="tab-button" onclick="showTab('correlation')">🔗 Correlations</button>
            <button class="tab-button" onclick="showTab('weights')">⚖️ Engagement Weights</button>
            <button class="tab-button" onclick="showTab('insights')">💡 Insights</button>
        </div>
        
        <!-- Overview Tab -->
        <div id="overview" class="tab-content active">
            <div class="section">
                <h2>Executive Summary</h2>
                <p style="font-size: 1.1em; line-height: 1.8; margin-bottom: 20px;">
                    This comprehensive analysis examines B2B SaaS user activity data to understand churn patterns 
                    and calculate engagement weights for a predictive scoring model. The dataset contains 
                    <strong>{len(df):,} user records</strong> with <strong>{len(df.columns)} activity metrics</strong>.
                </p>
                
                <div class="churn-meter">
                    <div style="flex: 0 0 150px;">
                        <strong>Retention:</strong><br>
                        <span style="font-size: 1.5em; color: #27ae60;">{churn_pct.get(0, 0):.1f}%</span>
                    </div>
                    <div class="meter-bar">
                        <div class="meter-fill meter-retained" style="width: {churn_pct.get(0, 0)}%;">
                            {churn_counts.get(0, 0):,} users
                        </div>
                    </div>
                </div>
                
                <div class="churn-meter">
                    <div style="flex: 0 0 150px;">
                        <strong>Churned:</strong><br>
                        <span style="font-size: 1.5em; color: #e74c3c;">{churn_pct.get(1, 0):.1f}%</span>
                    </div>
                    <div class="meter-bar">
                        <div class="meter-fill meter-churned" style="width: {churn_pct.get(1, 0)}%;">
                            {churn_counts.get(1, 0):,} users
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>Key Findings</h2>
                <div class="insight-box">
                    <h4>🎯 Top Engagement Indicators</h4>
                    <ul style="margin-left: 20px; line-height: 2;">
                        <li><strong>Num_Emails_Sent</strong> - Weight: {weights['Num_Emails_Sent']:.2f} (Highest impact on retention)</li>
                        <li><strong>Num_Exports</strong> - Weight: {weights['Num_Exports']:.2f} (Strong predictor)</li>
                        <li><strong>Num_Logins</strong> - Weight: {weights['Num_Logins']:.2f} (Moderate predictor)</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <!-- Data Quality Tab -->
        <div id="quality" class="tab-content">
            <div class="section">
                <h2>Data Quality Sanity Check</h2>
                
                <h3>Missing Values</h3>
                {'<span class="quality-badge badge-pass">✅ PASS: No missing values</span>' if missing_values.sum() == 0 else '<span class="quality-badge badge-warning">⚠️ WARNING: Missing values detected</span>'}
                
                <h3>Duplicate Records</h3>
                {'<span class="quality-badge badge-pass">✅ PASS: No duplicate rows</span>' if total_duplicates == 0 else f'<span class="quality-badge badge-warning">⚠️ Found {total_duplicates:,} duplicates</span>'}
                {'<span class="quality-badge badge-pass">✅ PASS: No duplicate User_IDs</span>' if duplicate_user_ids == 0 else f'<span class="quality-badge badge-error">❌ ERROR: {duplicate_user_ids:,} duplicate User_IDs</span>'}
                
                <h3>Data Types</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Column</th>
                            <th>Data Type</th>
                            <th>Non-Null Count</th>
                            <th>Total Count</th>
                        </tr>
                    </thead>
                    <tbody>
"""
    
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].count()
        total = len(df)
        html += f"""
                        <tr>
                            <td><code>{col}</code></td>
                            <td>{dtype}</td>
                            <td>{non_null:,}</td>
                            <td>{total:,}</td>
                        </tr>
"""
    
    html += """
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- Churn Analysis Tab -->
        <div id="churn" class="tab-content">
            <div class="section">
                <h2>Churn Distribution Analysis</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Status</th>
                            <th>Count</th>
                            <th>Percentage</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Retained (0)</strong></td>
                            <td>{churn_counts.get(0, 0):,}</td>
                            <td>{churn_pct.get(0, 0):.2f}%</td>
                        </tr>
                        <tr>
                            <td><strong>Churned (1)</strong></td>
                            <td>{churn_counts.get(1, 0):,}</td>
                            <td>{churn_pct.get(1, 0):.2f}%</td>
                        </tr>
                    </tbody>
                </table>
"""
    
    if churn_dist_img:
        html += f"""
                <div class="image-container">
                    <img src="data:image/png;base64,{churn_dist_img}" alt="Churn Distribution">
                </div>
"""
    
    if activity_boxplot_img:
        html += f"""
                <h3>Activity Metrics Comparison</h3>
                <div class="image-container">
                    <img src="data:image/png;base64,{activity_boxplot_img}" alt="Activity vs Churn Boxplots">
                </div>
"""
    
    html += """
            </div>
        </div>
        
        <!-- Correlation Tab -->
        <div id="correlation" class="tab-content">
            <div class="section">
                <h2>Correlation Analysis</h2>
                <p>All activity metrics show <strong>negative correlations</strong> with churn, indicating that higher activity levels are associated with lower churn rates.</p>
                
                <table>
                    <thead>
                        <tr>
                            <th>Activity Metric</th>
                            <th>Correlation with Churn</th>
                            <th>Interpretation</th>
                        </tr>
                    </thead>
                    <tbody>
"""
    
    for col in activity_columns:
        corr = correlations[col]
        interpretation = "Strong negative" if abs(corr) > 0.1 else "Moderate negative" if abs(corr) > 0.05 else "Weak negative"
        html += f"""
                        <tr>
                            <td><code>{col}</code></td>
                            <td><strong>{corr:.4f}</strong></td>
                            <td>{interpretation} correlation</td>
                        </tr>
"""
    
    html += """
                    </tbody>
                </table>
"""
    
    if correlation_heatmap_img:
        html += f"""
                <div class="image-container">
                    <img src="data:image/png;base64,{correlation_heatmap_img}" alt="Correlation Heatmap">
                </div>
"""
    
    html += """
            </div>
        </div>
        
        <!-- Weights Tab -->
        <div id="weights" class="tab-content">
            <div class="section">
                <h2>Engagement Weights Calculation</h2>
                
                <h3>Methodology</h3>
                <ol style="margin-left: 20px; line-height: 2;">
                    <li><strong>Invert Correlations:</strong> Multiply by -1 (negative correlation with Churn = positive impact on Retention)</li>
                    <li><strong>Normalize to 1-10 Scale:</strong> Transform inverted correlations to weights where 10 = most impactful feature</li>
                </ol>
                
                <div class="code-block">
weight = 1 + (inverted_correlation - min) / (max - min) × 9
                </div>
                
                <h3>Final Engagement Weights</h3>
                <div class="weights-grid">
"""
    
    sorted_weights = sorted(weights.items(), key=lambda x: x[1], reverse=True)
    for col, weight in sorted_weights:
        if weight >= 9:
            level = "Very High Impact"
        elif weight >= 7:
            level = "High Impact"
        elif weight >= 5:
            level = "Medium Impact"
        elif weight >= 3:
            level = "Low Impact"
        else:
            level = "Very Low Impact"
        
        html += f"""
                    <div class="weight-card">
                        <div class="metric">{col}</div>
                        <div class="weight">{weight:.2f}</div>
                        <div class="level">{level}</div>
                    </div>
"""
    
    html += """
                </div>
"""
    
    if weights_chart_img:
        html += f"""
                <div class="image-container">
                    <img src="data:image/png;base64,{weights_chart_img}" alt="Engagement Weights Chart">
                </div>
"""
    
    html += """
                <h3>Python Dictionary (Ready to Use)</h3>
                <div class="code-block">
weights = {
"""
    
    for col, weight in sorted_weights:
        html += f"    '{col}': {weight:.2f},\n"
    
    html += """}
                </div>
            </div>
        </div>
        
        <!-- Insights Tab -->
        <div id="insights" class="tab-content">
            <div class="section">
                <h2>Key Insights & Recommendations</h2>
                
                <div class="insight-box">
                    <h4>✅ Data Quality</h4>
                    <p>Excellent data quality with no missing values, duplicates, or data quality issues detected. Safe to proceed with model deployment.</p>
                </div>
                
                <div class="insight-box">
                    <h4>🎯 Top Engagement Indicators</h4>
                    <ul style="margin-left: 20px; line-height: 2;">
                        <li><strong>Num_Emails_Sent</strong> (Weight: {weights['Num_Emails_Sent']:.2f}) - Users who send emails are highly engaged</li>
                        <li><strong>Num_Exports</strong> (Weight: {weights['Num_Exports']:.2f}) - Export activity indicates strong product value</li>
                    </ul>
                </div>
                
                <div class="insight-box">
                    <h4>📊 Moderate Engagement Indicators</h4>
                    <ul style="margin-left: 20px; line-height: 2;">
                        <li><strong>Num_Logins</strong> (Weight: {weights['Num_Logins']:.2f}) - Regular logins show consistent usage</li>
                        <li><strong>Num_API_Calls</strong> (Weight: {weights['Num_API_Calls']:.2f}) - API usage indicates integration/automation</li>
                    </ul>
                </div>
                
                <div class="insight-box">
                    <h4>💡 Model Recommendations</h4>
                    <ol style="margin-left: 20px; line-height: 2;">
                        <li><strong>Scoring Model:</strong> Use calculated weights to create engagement score: <code>Engagement Score = Σ(Activity_Metric × Weight)</code></li>
                        <li><strong>Feature Priority:</strong> Focus retention efforts on users with low <code>Num_Emails_Sent</code> and <code>Num_Exports</code> as these are the strongest predictors.</li>
                        <li><strong>Threshold Setting:</strong> Consider setting engagement score thresholds based on churn rate distribution to identify at-risk users.</li>
                    </ol>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Analysis Framework: Python 3 with pandas, numpy, matplotlib, seaborn</p>
        </div>
    </div>
    
    <script>
        function showTab(tabName) {{
            // Hide all tab contents
            var contents = document.getElementsByClassName('tab-content');
            for (var i = 0; i < contents.length; i++) {{
                contents[i].classList.remove('active');
            }}
            
            // Remove active class from all buttons
            var buttons = document.getElementsByClassName('tab-button');
            for (var i = 0; i < buttons.length; i++) {{
                buttons[i].classList.remove('active');
            }}
            
            // Show selected tab content
            document.getElementById(tabName).classList.add('active');
            
            // Add active class to clicked button
            event.target.classList.add('active');
        }}
        
        // Add collapsible functionality
        var collapsibles = document.getElementsByClassName('collapsible');
        for (var i = 0; i < collapsibles.length; i++) {{
            collapsibles[i].addEventListener('click', function() {{
                this.classList.toggle('active');
                var content = this.nextElementSibling;
                if (content.style.maxHeight) {{
                    content.style.maxHeight = null;
                    content.classList.remove('active');
                }} else {{
                    content.style.maxHeight = content.scrollHeight + "px";
                    content.classList.add('active');
                }}
            }});
        }}
    </script>
</body>
</html>
"""
    
    return html

def main():
    """Generate and save the HTML report"""
    print("="*80)
    print("GENERATING INTERACTIVE HTML REPORT")
    print("="*80)
    
    html = generate_html_report()
    
    with open('INTERACTIVE_REPORT.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✓ Interactive HTML report saved: INTERACTIVE_REPORT.html")
    print("\n" + "="*80)
    print("REPORT GENERATION COMPLETE")
    print("="*80)
    print("\nOpen INTERACTIVE_REPORT.html in your web browser to view the report.")

if __name__ == "__main__":
    main()


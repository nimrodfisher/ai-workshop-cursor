"""
HTML Report Generation Template

This script generates a branded HTML analysis report with:
- Base64-embedded profile image
- ECharts visualizations
- Complete branding and styling
- Self-contained HTML file

Usage:
    1. Copy this file to your analysis folder
    2. Update the analysis data section with your data
    3. Run: py generate_html_report.py (Windows) or python3 generate_html_report.py (Unix)
    4. Delete the script after successful generation (optional)

Author: AI Analytics Hub
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# ============================================================================
# SETUP: Import utility functions for reliable path handling
# ============================================================================

# Add workspace root to path
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root))

try:
    # Import using absolute path from workspace root
    import importlib.util
    utils_path = workspace_root / ".cursor" / "utils" / "report_generator_utils.py"
    spec = importlib.util.spec_from_file_location("report_generator_utils", utils_path)
    report_utils = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(report_utils)
    
    # Import functions
    get_workspace_root = report_utils.get_workspace_root
    load_profile_image = report_utils.load_profile_image
    load_json_data = report_utils.load_json_data
    safe_write_file = report_utils.safe_write_file
    get_analysis_folder_path = report_utils.get_analysis_folder_path
    validate_data_files = report_utils.validate_data_files
except Exception as e:
    print(f"Error: Could not import utility functions: {e}")
    print(f"Ensure .cursor/utils/report_generator_utils.py exists at {workspace_root / '.cursor' / 'utils' / 'report_generator_utils.py'}")
    sys.exit(1)

# ============================================================================
# PATH SETUP: Automatic path resolution
# ============================================================================

script_path = Path(__file__)
analysis_folder = get_analysis_folder_path(script_path)
workspace_root = get_workspace_root(script_path)
data_dir = analysis_folder / "data"

# ============================================================================
# 1. LOAD PROFILE IMAGE (handles path resolution automatically)
# ============================================================================

profile_b64 = load_profile_image(workspace_root)

# ============================================================================
# 2. VALIDATE AND LOAD DATA FILES
# ============================================================================

# List your required data files here
required_files = [
    # "01_your-data.json",
    # Add more required files as needed
]

# Validate files exist (optional - comment out if not using data files)
# validation_results = validate_data_files(data_dir, required_files)
# if not all(validation_results.values()):
#     print("Error: Missing required data files. Cannot generate report.")
#     sys.exit(1)

# Load your data files (example - customize as needed)
# demographics = load_json_data(data_dir, "01_bug-reporters-demographics.json")
# behavior = load_json_data(data_dir, "02_bug-reporters-user-behavior.json")

# ============================================================================
# 3. PREPARE YOUR ANALYSIS DATA
# ============================================================================
# Replace this section with your actual analysis data

# Example: Data from SQL query or calculations
analysis_title = "Your Analysis Title"
analysis_date = datetime.now().strftime('%B %d, %Y')

# Example: Key metrics
metrics = {
    "total_growth": 29.5,
    "metric_1": 52.1,
    "metric_2": 30.7,
    "metric_3": 11.9
}

# Example: Chart data
chart_months = ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06',
                '2025-07', '2025-08', '2025-09', '2025-10', '2025-11', '2025-12']

chart_series_1 = [2822, 3067, 3183, 2897, 3158, 3158, 3158, 3158, 3158, 3158, 3158, 3158]
chart_series_2 = [2053, 2480, 2986, 2907, 3123, 3123, 3123, 3123, 3123, 3123, 3123, 3123]
chart_series_3 = [2327, 2854, 3609, 3398, 3120, 3041, 3041, 3041, 3041, 3041, 3041, 3041]

# ============================================================================
# 3. GENERATE HTML CONTENT
# ============================================================================

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{analysis_title} | AI Analytics Hub</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        :root {{
            --color-primary: #2563EB;
            --color-primary-dark: #1E40AF;
            --color-secondary: #0EA5E9;
            --color-bg: #F8FAFC;
            --color-surface: #FFFFFF;
            --color-text: #1E293B;
            --color-text-secondary: #64748B;
            --color-border: #E2E8F0;
            --color-success: #10B981;
            --color-warning: #F59E0B;
            --color-error: #EF4444;
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: var(--font-sans);
            font-size: 16px;
            line-height: 1.6;
            color: var(--color-text);
            background: var(--color-bg);
            padding: 2rem;
        }}

        .report-container {{
            max-width: 1000px;
            margin: 0 auto;
            background: var(--color-surface);
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }}

        .report-header {{
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
            color: white;
            padding: 2rem 2.5rem;
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }}

        .report-header img.profile {{
            width: 64px;
            height: 64px;
            border-radius: 50%;
            border: 3px solid rgba(255,255,255,0.3);
            object-fit: cover;
        }}

        .report-header-content {{
            flex: 1;
        }}

        .report-header h1 {{
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }}

        .report-header .meta {{
            font-size: 0.875rem;
            opacity: 0.9;
        }}

        .report-body {{
            padding: 2.5rem;
        }}

        .section {{
            margin-bottom: 2.5rem;
            page-break-inside: avoid;
        }}

        .section-title {{
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--color-primary);
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--color-border);
        }}

        .executive-summary {{
            background: linear-gradient(135deg, #EFF6FF 0%, #F0F9FF 100%);
            border-left: 4px solid var(--color-primary);
            padding: 1.5rem;
            border-radius: 0 8px 8px 0;
            margin: 1.5rem 0;
        }}

        .recommendations {{
            background: linear-gradient(135deg, #ECFDF5 0%, #F0FDFA 100%);
            border-left: 4px solid var(--color-success);
            padding: 1.5rem;
            border-radius: 0 8px 8px 0;
            margin: 1.5rem 0;
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;
        }}

        .metric-card {{
            background: var(--color-bg);
            border: 1px solid var(--color-border);
            border-radius: 8px;
            padding: 1.25rem;
            text-align: center;
        }}

        .metric-card .value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--color-primary);
            margin-bottom: 0.25rem;
        }}

        .metric-card.positive .value {{
            color: var(--color-success);
        }}

        .metric-card.negative .value {{
            color: var(--color-error);
        }}

        .metric-card .label {{
            font-size: 0.875rem;
            color: var(--color-text-secondary);
            font-weight: 500;
        }}

        .chart-container {{
            border: 1px solid var(--color-border);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            background: var(--color-surface);
        }}

        .chart-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--color-text);
            margin-bottom: 1rem;
        }}

        .chart {{
            width: 100%;
            height: 400px;
        }}

        .callout {{
            padding: 1rem 1.25rem;
            border-radius: 8px;
            margin: 1rem 0;
        }}

        .callout.info {{
            background: #EFF6FF;
            border-left: 4px solid var(--color-primary);
        }}

        .callout.warning {{
            background: #FFFBEB;
            border-left: 4px solid var(--color-warning);
        }}

        .callout.success {{
            background: #ECFDF5;
            border-left: 4px solid var(--color-success);
        }}

        .report-footer {{
            background: var(--color-bg);
            padding: 1.5rem 2.5rem;
            text-align: center;
            border-top: 1px solid var(--color-border);
            font-size: 0.875rem;
            color: var(--color-text-secondary);
        }}

        @media print {{
            body {{ background: white; padding: 0; }}
            .report-container {{ box-shadow: none; }}
            .section {{ page-break-inside: avoid; }}
        }}
    </style>
</head>
<body>
    <div class="report-container">
        <!-- Header with Profile Image -->
        <div class="report-header">
            {f'<img src="{profile_b64}" alt="Profile" class="profile">' if profile_b64 else ''}
            <div class="report-header-content">
                <h1>{analysis_title}</h1>
                <div class="meta">{analysis_date} • Nimrod Fisher | AI Analytics Hub</div>
            </div>
        </div>

        <div class="report-body">
            <!-- Executive Summary -->
            <div class="section">
                <div class="section-title">Executive Summary</div>
                <div class="executive-summary">
                    <p><strong>Key finding summary goes here.</strong> Add your analysis summary with the most important insights.</p>
                </div>

                <!-- Metrics Grid -->
                <div class="metrics-grid">
                    <div class="metric-card positive">
                        <div class="value">+{metrics['total_growth']:.1f}%</div>
                        <div class="label">Total Growth</div>
                    </div>
                    <div class="metric-card positive">
                        <div class="value">+{metrics['metric_1']:.1f}%</div>
                        <div class="label">Metric 1</div>
                    </div>
                    <div class="metric-card positive">
                        <div class="value">+{metrics['metric_2']:.1f}%</div>
                        <div class="label">Metric 2</div>
                    </div>
                    <div class="metric-card positive">
                        <div class="value">+{metrics['metric_3']:.1f}%</div>
                        <div class="label">Metric 3</div>
                    </div>
                </div>
            </div>

            <!-- Methodology -->
            <div class="section">
                <div class="section-title">Methodology</div>
                <p><strong>Data Sources:</strong> Your data sources</p>
                <p><strong>Analysis Period:</strong> Your time period</p>
                <p><strong>Approach:</strong> Your methodology</p>
                <div class="callout info">
                    <strong>Note:</strong> Any important caveats or limitations
                </div>
            </div>

            <!-- Findings with Charts -->
            <div class="section">
                <div class="section-title">Findings</div>

                <!-- Example Chart -->
                <div class="chart-container">
                    <div class="chart-title">Your Chart Title</div>
                    <div id="chart1" class="chart"></div>
                </div>

                <!-- Insights -->
                <div class="callout success">
                    <strong>Key Insight:</strong> Your main finding
                </div>

                <div class="callout warning">
                    <strong>Note:</strong> Something to watch
                </div>
            </div>

            <!-- Recommendations -->
            <div class="section">
                <div class="section-title">Recommendations</div>
                <div class="recommendations">
                    <h3 style="margin-bottom: 1rem; font-size: 1.1rem; font-weight: 600;">Immediate Actions</h3>
                    <ul style="margin-left: 1.5rem; margin-top: 0.5rem;">
                        <li style="margin-bottom: 0.5rem;"><strong>Action 1:</strong> Description</li>
                        <li style="margin-bottom: 0.5rem;"><strong>Action 2:</strong> Description</li>
                    </ul>

                    <h3 style="margin-top: 1.5rem; margin-bottom: 1rem; font-size: 1.1rem; font-weight: 600;">Long-term</h3>
                    <ul style="margin-left: 1.5rem; margin-top: 0.5rem;">
                        <li style="margin-bottom: 0.5rem;">Strategic recommendation 1</li>
                        <li style="margin-bottom: 0.5rem;">Strategic recommendation 2</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="report-footer">
            The Analytics Team • ai-analytics-hub.com
        </div>
    </div>

    <!-- Charts JavaScript -->
    <script>
        // Example Chart with ECharts
        var chart1 = echarts.init(document.getElementById('chart1'));
        var option1 = {{
            tooltip: {{
                trigger: 'axis',
                axisPointer: {{ type: 'cross' }}
            }},
            legend: {{
                data: ['Series 1', 'Series 2', 'Series 3'],
                top: 10
            }},
            grid: {{
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            }},
            xAxis: {{
                type: 'category',
                boundaryGap: false,
                data: {json.dumps(chart_months)}
            }},
            yAxis: {{
                type: 'value',
                axisLabel: {{ formatter: '${{value}}' }}
            }},
            series: [
                {{
                    name: 'Series 1',
                    type: 'line',
                    smooth: true,
                    data: {json.dumps(chart_series_1)},
                    itemStyle: {{ color: '#2563EB' }},
                    lineStyle: {{ width: 3 }}
                }},
                {{
                    name: 'Series 2',
                    type: 'line',
                    smooth: true,
                    data: {json.dumps(chart_series_2)},
                    itemStyle: {{ color: '#0EA5E9' }},
                    lineStyle: {{ width: 3 }}
                }},
                {{
                    name: 'Series 3',
                    type: 'line',
                    smooth: true,
                    data: {json.dumps(chart_series_3)},
                    itemStyle: {{ color: '#10B981' }},
                    lineStyle: {{ width: 3 }}
                }}
            ]
        }};
        chart1.setOption(option1);

        // Handle window resize
        window.addEventListener('resize', function() {{
            chart1.resize();
        }});
    </script>
</body>
</html>
"""

# ============================================================================
# 4. SAVE REPORT (automatic path resolution and error handling)
# ============================================================================

output_path = analysis_folder / "deliverables" / "report.html"

if safe_write_file(output_path, html_content):
    print(f"[SUCCESS] HTML report generated: {output_path.absolute()}")
    print(f"[INFO] File size: {output_path.stat().st_size:,} bytes")
else:
    print(f"[ERROR] Failed to generate report")
    sys.exit(1)







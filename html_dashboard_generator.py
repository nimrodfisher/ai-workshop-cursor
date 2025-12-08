"""
HTML Dashboard Generator
Creates static HTML dashboard mockups from analysis results
"""

from typing import Dict, List, Any, Optional
import json
from datetime import datetime
import base64


class HTMLDashboardGenerator:
    """
    Generates interactive HTML dashboards from analysis results
    Creates standalone HTML files that can be opened in any browser
    """
    
    def __init__(self):
        self.charts = []
        self.metrics = []
        self.tables = []
        self.title = "Analysis Dashboard"
        self.description = ""
        
    def add_metric(self, label: str, value: Any, format: str = "number", 
                   change: Optional[float] = None, change_label: str = ""):
        """Add a metric card to the dashboard"""
        self.metrics.append({
            'label': label,
            'value': value,
            'format': format,  # 'number', 'currency', 'percentage'
            'change': change,
            'change_label': change_label
        })
    
    def add_chart(self, chart_type: str, data: List[Dict], title: str, 
                  x_column: str, y_column: str, color_column: Optional[str] = None):
        """
        Add a chart to the dashboard
        
        Args:
            chart_type: 'bar', 'line', 'pie', 'scatter'
            data: List of dictionaries with chart data
            title: Chart title
            x_column: Column name for x-axis
            y_column: Column name for y-axis
            color_column: Optional column for color coding
        """
        self.charts.append({
            'type': chart_type,
            'data': data,
            'title': title,
            'x_column': x_column,
            'y_column': y_column,
            'color_column': color_column
        })
    
    def add_table(self, data: List[Dict], title: str, columns: Optional[List[str]] = None):
        """Add a data table to the dashboard"""
        if columns is None and data:
            columns = list(data[0].keys())
        
        self.tables.append({
            'title': title,
            'data': data,
            'columns': columns or []
        })
    
    def format_value(self, value: Any, format_type: str) -> str:
        """Format value based on format type"""
        if value is None:
            return "N/A"
        
        if format_type == "currency":
            return f"${float(value):,.2f}"
        elif format_type == "percentage":
            return f"{float(value):.2f}%"
        elif format_type == "number":
            if isinstance(value, (int, float)):
                return f"{value:,.0f}" if value == int(value) else f"{value:,.2f}"
            return str(value)
        else:
            return str(value)
    
    def generate_chart_js(self, chart: Dict) -> str:
        """Generate Chart.js code for a chart"""
        chart_id = f"chart_{len(self.charts)}"
        data_json = json.dumps(chart['data'])
        
        if chart['type'] == 'bar':
            return f"""
            <canvas id="{chart_id}"></canvas>
            <script>
                const ctx_{chart_id} = document.getElementById('{chart_id}').getContext('2d');
                const data_{chart_id} = {data_json};
                new Chart(ctx_{chart_id}, {{
                    type: 'bar',
                    data: {{
                        labels: data_{chart_id}.map(d => d['{chart['x_column']}']),
                        datasets: [{{
                            label: '{chart['y_column']}',
                            data: data_{chart_id}.map(d => d['{chart['y_column']}']),
                            backgroundColor: 'rgba(54, 162, 235, 0.6)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        plugins: {{
                            title: {{
                                display: true,
                                text: '{chart['title']}'
                            }}
                        }}
                    }}
                }});
            </script>
            """
        
        elif chart['type'] == 'line':
            return f"""
            <canvas id="{chart_id}"></canvas>
            <script>
                const ctx_{chart_id} = document.getElementById('{chart_id}').getContext('2d');
                const data_{chart_id} = {data_json};
                new Chart(ctx_{chart_id}, {{
                    type: 'line',
                    data: {{
                        labels: data_{chart_id}.map(d => d['{chart['x_column']}']),
                        datasets: [{{
                            label: '{chart['y_column']}',
                            data: data_{chart_id}.map(d => d['{chart['y_column']}']),
                            borderColor: 'rgba(75, 192, 192, 1)',
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            tension: 0.1
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        plugins: {{
                            title: {{
                                display: true,
                                text: '{chart['title']}'
                            }}
                        }}
                    }}
                }});
            </script>
            """
        
        elif chart['type'] == 'pie':
            return f"""
            <canvas id="{chart_id}"></canvas>
            <script>
                const ctx_{chart_id} = document.getElementById('{chart_id}').getContext('2d');
                const data_{chart_id} = {data_json};
                new Chart(ctx_{chart_id}, {{
                    type: 'pie',
                    data: {{
                        labels: data_{chart_id}.map(d => d['{chart['x_column']}']),
                        datasets: [{{
                            data: data_{chart_id}.map(d => d['{chart['y_column']}']),
                            backgroundColor: [
                                'rgba(255, 99, 132, 0.6)',
                                'rgba(54, 162, 235, 0.6)',
                                'rgba(255, 206, 86, 0.6)',
                                'rgba(75, 192, 192, 0.6)',
                                'rgba(153, 102, 255, 0.6)',
                                'rgba(255, 159, 64, 0.6)'
                            ]
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        plugins: {{
                            title: {{
                                display: true,
                                text: '{chart['title']}'
                            }}
                        }}
                    }}
                }});
            </script>
            """
        
        return ""
    
    def generate_html(self) -> str:
        """Generate complete HTML dashboard"""
        
        # Generate metrics HTML
        metrics_html = ""
        if self.metrics:
            metrics_html = '<div class="metrics-grid">'
            for metric in self.metrics:
                change_html = ""
                if metric['change'] is not None:
                    change_class = "positive" if metric['change'] >= 0 else "negative"
                    change_html = f'<div class="change {change_class}">{metric["change_label"]} {abs(metric["change"]):.1f}%</div>'
                
                metrics_html += f"""
                <div class="metric-card">
                    <div class="metric-label">{metric['label']}</div>
                    <div class="metric-value">{self.format_value(metric['value'], metric['format'])}</div>
                    {change_html}
                </div>
                """
            metrics_html += '</div>'
        
        # Generate charts HTML
        charts_html = ""
        for i, chart in enumerate(self.charts):
            charts_html += f'<div class="chart-container"><div class="chart-wrapper">{self.generate_chart_js(chart)}</div></div>'
        
        # Generate tables HTML
        tables_html = ""
        for table in self.tables:
            # Build table header
            header_html = '<thead><tr>'
            for col in table['columns']:
                header_html += f'<th>{col}</th>'
            header_html += '</tr></thead>'
            
            # Build table body
            body_html = '<tbody>'
            for row in table['data']:
                body_html += '<tr>'
                for col in table['columns']:
                    value = row.get(col, '')
                    # Format numeric values
                    if isinstance(value, (int, float)):
                        if value == int(value):
                            value = f"{int(value):,}"
                        else:
                            value = f"{value:,.2f}"
                    body_html += f'<td>{value}</td>'
                body_html += '</tr>'
            body_html += '</tbody>'
            
            tables_html += f"""
            <div class="table-container">
                <h3>{table['title']}</h3>
                <table class="data-table">
                    {header_html}
                    {body_html}
                </table>
            </div>
            """
        
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f7fa;
            color: #333;
            padding: 20px;
        }}
        
        .dashboard-header {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        
        .dashboard-header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
            color: #1a1a1a;
        }}
        
        .dashboard-header p {{
            color: #666;
            font-size: 16px;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #4a90e2;
        }}
        
        .metric-label {{
            font-size: 14px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
        }}
        
        .metric-value {{
            font-size: 32px;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 5px;
        }}
        
        .change {{
            font-size: 12px;
            font-weight: 500;
        }}
        
        .change.positive {{
            color: #27ae60;
        }}
        
        .change.negative {{
            color: #e74c3c;
        }}
        
        .chart-container {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        
        .chart-wrapper {{
            position: relative;
            height: 400px;
        }}
        
        .table-container {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            overflow-x: auto;
        }}
        
        .table-container h3 {{
            margin-bottom: 20px;
            color: #1a1a1a;
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .data-table th {{
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #333;
            border-bottom: 2px solid #dee2e6;
        }}
        
        .data-table td {{
            padding: 12px;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .data-table tr:hover {{
            background: #f8f9fa;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="dashboard-header">
        <h1>{self.title}</h1>
        <p>{self.description or "Generated from analysis results"}</p>
        <p style="margin-top: 10px; font-size: 14px; color: #999;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    {metrics_html}
    
    {charts_html}
    
    {tables_html}
    
    <div class="footer">
        <p>Dashboard generated by Analysis Framework</p>
    </div>
</body>
</html>
        """
        
        return html_template
    
    def save_dashboard(self, filepath: str):
        """Save dashboard to HTML file"""
        html_content = self.generate_html()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return filepath


def create_dashboard_from_analysis(analysis_results: Dict[str, Any], 
                                    title: str = "Analysis Dashboard") -> str:
    """
    Create HTML dashboard from analysis framework results
    
    Args:
        analysis_results: Results from analysis framework
        title: Dashboard title
    
    Returns:
        Path to saved HTML file
    """
    generator = HTMLDashboardGenerator()
    generator.title = title
    generator.description = f"Analysis results from {len(analysis_results.get('steps', []))} steps"
    
    # Extract metrics from analysis steps
    for step in analysis_results.get('steps', []):
        if step.get('row_count'):
            generator.add_metric(
                label=f"Step {step['step_number']} - Rows",
                value=step['row_count'],
                format="number"
            )
    
    # Add execution time metric
    if analysis_results.get('total_execution_time'):
        generator.add_metric(
            label="Total Execution Time",
            value=f"{analysis_results['total_execution_time']:.2f}s",
            format="number"
        )
    
    # Save and return path
    filepath = f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    generator.save_dashboard(filepath)
    return filepath




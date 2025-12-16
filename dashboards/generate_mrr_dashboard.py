"""
Generate MRR by Plan Over Time Dashboard
"""

from html_dashboard_generator import HTMLDashboardGenerator
from datetime import datetime
import json

# Query results from the database
query_results = [
    {"month":"2025-12-01 00:00:00+00","plan":"free","mrr":"3158.00","subscription_count":32,"previous_month_mrr":"3158","mrr_change_percent":"0.00"},
    {"month":"2025-12-01 00:00:00+00","plan":"pro","mrr":"3123.00","subscription_count":27,"previous_month_mrr":"3123","mrr_change_percent":"0.00"},
    {"month":"2025-12-01 00:00:00+00","plan":"enterprise","mrr":"3041.00","subscription_count":29,"previous_month_mrr":"3041","mrr_change_percent":"0.00"},
    {"month":"2025-11-01 00:00:00+00","plan":"free","mrr":"3158.00","subscription_count":32,"previous_month_mrr":"3158","mrr_change_percent":"0.00"},
    {"month":"2025-11-01 00:00:00+00","plan":"pro","mrr":"3123.00","subscription_count":27,"previous_month_mrr":"3123","mrr_change_percent":"0.00"},
    {"month":"2025-11-01 00:00:00+00","plan":"enterprise","mrr":"3041.00","subscription_count":29,"previous_month_mrr":"3041","mrr_change_percent":"0.00"},
    {"month":"2025-10-01 00:00:00+00","plan":"free","mrr":"3158.00","subscription_count":32,"previous_month_mrr":"3158","mrr_change_percent":"0.00"},
    {"month":"2025-10-01 00:00:00+00","plan":"pro","mrr":"3123.00","subscription_count":27,"previous_month_mrr":"3123","mrr_change_percent":"0.00"},
    {"month":"2025-10-01 00:00:00+00","plan":"enterprise","mrr":"3041.00","subscription_count":29,"previous_month_mrr":"3041","mrr_change_percent":"0.00"},
    {"month":"2025-09-01 00:00:00+00","plan":"free","mrr":"3158.00","subscription_count":32,"previous_month_mrr":"3158","mrr_change_percent":"0.00"},
    {"month":"2025-09-01 00:00:00+00","plan":"pro","mrr":"3123.00","subscription_count":27,"previous_month_mrr":"3123","mrr_change_percent":"0.00"},
    {"month":"2025-09-01 00:00:00+00","plan":"enterprise","mrr":"3041.00","subscription_count":29,"previous_month_mrr":"3041","mrr_change_percent":"0.00"},
    {"month":"2025-08-01 00:00:00+00","plan":"free","mrr":"3158.00","subscription_count":32,"previous_month_mrr":"3158","mrr_change_percent":"0.00"},
    {"month":"2025-08-01 00:00:00+00","plan":"pro","mrr":"3123.00","subscription_count":27,"previous_month_mrr":"3123","mrr_change_percent":"0.00"},
    {"month":"2025-08-01 00:00:00+00","plan":"enterprise","mrr":"3041.00","subscription_count":29,"previous_month_mrr":"3041","mrr_change_percent":"0.00"},
    {"month":"2025-07-01 00:00:00+00","plan":"free","mrr":"3158.00","subscription_count":32,"previous_month_mrr":"3158","mrr_change_percent":"0.00"},
    {"month":"2025-07-01 00:00:00+00","plan":"pro","mrr":"3123.00","subscription_count":27,"previous_month_mrr":"3123","mrr_change_percent":"0.00"},
    {"month":"2025-07-01 00:00:00+00","plan":"enterprise","mrr":"3041.00","subscription_count":29,"previous_month_mrr":"3041","mrr_change_percent":"0.00"},
    {"month":"2025-06-01 00:00:00+00","plan":"free","mrr":"3158.00","subscription_count":32,"previous_month_mrr":"3158","mrr_change_percent":"0.00"},
    {"month":"2025-06-01 00:00:00+00","plan":"pro","mrr":"3123.00","subscription_count":27,"previous_month_mrr":"3123","mrr_change_percent":"0.00"},
    {"month":"2025-06-01 00:00:00+00","plan":"enterprise","mrr":"3041.00","subscription_count":29,"previous_month_mrr":"3120","mrr_change_percent":"-2.53"},
    {"month":"2025-05-01 00:00:00+00","plan":"free","mrr":"3158.00","subscription_count":32,"previous_month_mrr":"2897","mrr_change_percent":"9.01"},
    {"month":"2025-05-01 00:00:00+00","plan":"pro","mrr":"3123.00","subscription_count":27,"previous_month_mrr":"2907","mrr_change_percent":"7.43"},
    {"month":"2025-05-01 00:00:00+00","plan":"enterprise","mrr":"3120.00","subscription_count":30,"previous_month_mrr":"3398","mrr_change_percent":"-8.18"},
    {"month":"2025-04-01 00:00:00+00","plan":"enterprise","mrr":"3398.00","subscription_count":32,"previous_month_mrr":"3609","mrr_change_percent":"-5.85"},
    {"month":"2025-04-01 00:00:00+00","plan":"pro","mrr":"2907.00","subscription_count":23,"previous_month_mrr":"2986","mrr_change_percent":"-2.65"},
    {"month":"2025-04-01 00:00:00+00","plan":"free","mrr":"2897.00","subscription_count":33,"previous_month_mrr":"3183","mrr_change_percent":"-8.99"},
    {"month":"2025-03-01 00:00:00+00","plan":"enterprise","mrr":"3609.00","subscription_count":31,"previous_month_mrr":"2854","mrr_change_percent":"26.45"},
    {"month":"2025-03-01 00:00:00+00","plan":"free","mrr":"3183.00","subscription_count":37,"previous_month_mrr":"3067","mrr_change_percent":"3.78"},
    {"month":"2025-03-01 00:00:00+00","plan":"pro","mrr":"2986.00","subscription_count":24,"previous_month_mrr":"2480","mrr_change_percent":"20.40"},
    {"month":"2025-02-01 00:00:00+00","plan":"free","mrr":"3067.00","subscription_count":33,"previous_month_mrr":"2822","mrr_change_percent":"8.68"},
    {"month":"2025-02-01 00:00:00+00","plan":"enterprise","mrr":"2854.00","subscription_count":26,"previous_month_mrr":"2327","mrr_change_percent":"22.65"},
    {"month":"2025-02-01 00:00:00+00","plan":"pro","mrr":"2480.00","subscription_count":20,"previous_month_mrr":"2053","mrr_change_percent":"20.80"},
    {"month":"2025-01-01 00:00:00+00","plan":"free","mrr":"2822.00","subscription_count":28,"previous_month_mrr":"2573","mrr_change_percent":"9.68"},
    {"month":"2025-01-01 00:00:00+00","plan":"enterprise","mrr":"2327.00","subscription_count":23,"previous_month_mrr":"2248","mrr_change_percent":"3.51"},
    {"month":"2025-01-01 00:00:00+00","plan":"pro","mrr":"2053.00","subscription_count":17,"previous_month_mrr":"1576","mrr_change_percent":"30.27"},
    {"month":"2024-12-01 00:00:00+00","plan":"free","mrr":"2573.00","subscription_count":27,"previous_month_mrr":"1669","mrr_change_percent":"54.16"},
    {"month":"2024-12-01 00:00:00+00","plan":"enterprise","mrr":"2248.00","subscription_count":22,"previous_month_mrr":"1684","mrr_change_percent":"33.49"},
    {"month":"2024-12-01 00:00:00+00","plan":"pro","mrr":"1576.00","subscription_count":14,"previous_month_mrr":"1377","mrr_change_percent":"14.45"},
    {"month":"2024-11-01 00:00:00+00","plan":"enterprise","mrr":"1684.00","subscription_count":16,"previous_month_mrr":"1398","mrr_change_percent":"20.46"},
    {"month":"2024-11-01 00:00:00+00","plan":"free","mrr":"1669.00","subscription_count":21,"previous_month_mrr":"1669","mrr_change_percent":"0.00"},
    {"month":"2024-11-01 00:00:00+00","plan":"pro","mrr":"1377.00","subscription_count":13,"previous_month_mrr":"871","mrr_change_percent":"58.09"},
    {"month":"2024-10-01 00:00:00+00","plan":"free","mrr":"1669.00","subscription_count":21,"previous_month_mrr":"1511","mrr_change_percent":"10.46"},
    {"month":"2024-10-01 00:00:00+00","plan":"enterprise","mrr":"1398.00","subscription_count":12,"previous_month_mrr":"1091","mrr_change_percent":"28.14"},
    {"month":"2024-10-01 00:00:00+00","plan":"pro","mrr":"871.00","subscription_count":9,"previous_month_mrr":"763","mrr_change_percent":"14.15"},
    {"month":"2024-09-01 00:00:00+00","plan":"free","mrr":"1511.00","subscription_count":19,"previous_month_mrr":"938","mrr_change_percent":"61.09"},
    {"month":"2024-09-01 00:00:00+00","plan":"enterprise","mrr":"1091.00","subscription_count":9,"previous_month_mrr":"1012","mrr_change_percent":"7.81"},
    {"month":"2024-09-01 00:00:00+00","plan":"pro","mrr":"763.00","subscription_count":7,"previous_month_mrr":"734","mrr_change_percent":"3.95"},
    {"month":"2024-08-01 00:00:00+00","plan":"enterprise","mrr":"1012.00","subscription_count":8,"previous_month_mrr":"904","mrr_change_percent":"11.95"},
    {"month":"2024-08-01 00:00:00+00","plan":"free","mrr":"938.00","subscription_count":12,"previous_month_mrr":"245","mrr_change_percent":"282.86"},
    {"month":"2024-08-01 00:00:00+00","plan":"pro","mrr":"734.00","subscription_count":6,"previous_month_mrr":"904","mrr_change_percent":"-18.81"},
    {"month":"2024-07-01 00:00:00+00","plan":"enterprise","mrr":"904.00","subscription_count":6,"previous_month_mrr":"228","mrr_change_percent":"296.49"},
    {"month":"2024-07-01 00:00:00+00","plan":"pro","mrr":"904.00","subscription_count":6,"previous_month_mrr":"307","mrr_change_percent":"194.46"},
    {"month":"2024-07-01 00:00:00+00","plan":"free","mrr":"245.00","subscription_count":5,"previous_month_mrr":"137","mrr_change_percent":"78.83"},
    {"month":"2024-06-01 00:00:00+00","plan":"pro","mrr":"307.00","subscription_count":3,"previous_month_mrr":None,"mrr_change_percent":None},
    {"month":"2024-06-01 00:00:00+00","plan":"enterprise","mrr":"228.00","subscription_count":2,"previous_month_mrr":None,"mrr_change_percent":None},
    {"month":"2024-06-01 00:00:00+00","plan":"free","mrr":"137.00","subscription_count":3,"previous_month_mrr":None,"mrr_change_percent":None}
]

def parse_month(date_str):
    """Parse month from timestamp string"""
    if date_str:
        return datetime.fromisoformat(date_str.replace('+00:00', '+00:00')).strftime('%Y-%m')
    return None

def generate_dashboard():
    """Generate the MRR dashboard"""
    generator = HTMLDashboardGenerator()
    generator.title = "MRR Metrics by Plan Over Time"
    generator.description = "Monthly Recurring Revenue trends for Free, Pro, and Enterprise plans from June 2024 to December 2025"
    
    # Calculate summary metrics
    latest_month_data = [r for r in query_results if parse_month(r['month']) == '2025-12']
    total_mrr = sum(float(r['mrr']) for r in latest_month_data)
    
    # Calculate growth from first month to latest
    first_month_data = [r for r in query_results if parse_month(r['month']) == '2024-06']
    first_total_mrr = sum(float(r['mrr']) for r in first_month_data)
    total_growth = ((total_mrr - first_total_mrr) / first_total_mrr * 100) if first_total_mrr > 0 else 0
    
    # Add summary metrics
    generator.add_metric(
        label="Total MRR (Latest)",
        value=total_mrr,
        format="currency"
    )
    
    generator.add_metric(
        label="Total Growth (Since June 2024)",
        value=total_growth,
        format="percentage",
        change=total_growth,
        change_label="vs. June 2024"
    )
    
    # Prepare data for line chart - group by plan
    plans = ['free', 'pro', 'enterprise']
    chart_data = []
    
    # Sort by month
    sorted_results = sorted(query_results, key=lambda x: parse_month(x['month']) or '')
    
    # Create datasets for each plan
    for plan in plans:
        plan_data = [r for r in sorted_results if r['plan'] == plan]
        for row in plan_data:
            month_str = parse_month(row['month'])
            chart_data.append({
                'month': month_str,
                'plan': plan.capitalize(),
                'mrr': float(row['mrr'])
            })
    
    # Create line chart with multiple datasets (one per plan)
    # We need to format data for Chart.js multi-line chart
    months = sorted(set(parse_month(r['month']) for r in query_results if parse_month(r['month'])))
    
    # Generate Chart.js code for multi-line chart
    chart_id = "mrr_trend_chart"
    chart_js = f"""
    <canvas id="{chart_id}"></canvas>
    <script>
        const ctx_{chart_id} = document.getElementById('{chart_id}').getContext('2d');
        const months_{chart_id} = {json.dumps(months)};
        
        // Prepare data for each plan
        const freeData = {json.dumps([float(r['mrr']) for r in sorted_results if r['plan'] == 'free'])}; 
        const proData = {json.dumps([float(r['mrr']) for r in sorted_results if r['plan'] == 'pro'])}; 
        const enterpriseData = {json.dumps([float(r['mrr']) for r in sorted_results if r['plan'] == 'enterprise'])}; 
        
        new Chart(ctx_{chart_id}, {{
            type: 'line',
            data: {{
                labels: months_{chart_id},
                datasets: [
                    {{
                        label: 'Free Plan',
                        data: freeData,
                        borderColor: 'rgba(54, 162, 235, 1)',
                        backgroundColor: 'rgba(54, 162, 235, 0.1)',
                        tension: 0.1,
                        fill: false
                    }},
                    {{
                        label: 'Pro Plan',
                        data: proData,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'rgba(75, 192, 192, 0.1)',
                        tension: 0.1,
                        fill: false
                    }},
                    {{
                        label: 'Enterprise Plan',
                        data: enterpriseData,
                        borderColor: 'rgba(255, 99, 132, 1)',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        tension: 0.1,
                        fill: false
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    title: {{
                        display: true,
                        text: 'MRR Trends by Plan Over Time',
                        font: {{
                            size: 18
                        }}
                    }},
                    legend: {{
                        display: true,
                        position: 'top'
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return context.dataset.label + ': $' + context.parsed.y.toLocaleString('en-US', {{minimumFractionDigits: 2, maximumFractionDigits: 2}});
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return '$' + value.toLocaleString('en-US');
                            }}
                        }},
                        title: {{
                            display: true,
                            text: 'MRR ($)'
                        }}
                    }},
                    x: {{
                        title: {{
                            display: true,
                            text: 'Month'
                        }}
                    }}
                }}
            }}
        }});
    </script>
    """
    
    # Prepare table data
    table_data = []
    for row in sorted_results:
        month_str = parse_month(row['month'])
        change_pct = row.get('mrr_change_percent')
        change_str = f"{float(change_pct):.2f}%" if change_pct else "N/A"
        table_data.append({
            'Month': month_str,
            'Plan': row['plan'].capitalize(),
            'MRR': f"${float(row['mrr']):,.2f}",
            'Subscriptions': int(row['subscription_count']),
            'MoM Change': change_str
        })
    
    generator.add_table(
        data=table_data,
        title="MRR by Plan - Monthly Details",
        columns=['Month', 'Plan', 'MRR', 'Subscriptions', 'MoM Change']
    )
    
    # Add custom multi-line chart by modifying the HTML generation
    # We'll inject custom JS after the generator creates the HTML
    original_generate_html = generator.generate_html
    
    def custom_generate_html():
        html = original_generate_html()
        # Insert custom chart before tables
        chart_html = f"""
        <div class="chart-container">
            <div class="chart-wrapper" style="height: 500px;">
                {chart_js}
            </div>
        </div>
        """
        # Insert chart before tables
        html = html.replace('<div class="table-container">', chart_html + '<div class="table-container">')
        return html
    
    generator.generate_html = custom_generate_html
    
    # Save dashboard
    filepath = f"dashboard_mrr_by_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    generator.save_dashboard(filepath)
    print(f"✅ Dashboard created: {filepath}")
    return filepath

if __name__ == "__main__":
    generate_dashboard()


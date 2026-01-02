import json
import base64
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# Configuration & Branding
ANALYSIS_TITLE = "Bug Ticket User Analysis"
ANALYST_NAME = "Nimrod Fisher | AI Analytics Hub"
WEBSITE = "ai-analytics-hub.com"
FOOTER_TEXT = "The Analytics Team • ai-analytics-hub.com"
PRIMARY_COLOR = "#2563EB"
PRIMARY_DARK = "#1E40AF"
SECONDARY_COLOR = "#0EA5E9"
SUCCESS_COLOR = "#10B981"
WARNING_COLOR = "#F59E0B"
ERROR_COLOR = "#EF4444"

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DELIVERABLES_DIR = BASE_DIR / "deliverables"
ROOT_DIR = Path("../../")
PHOTO_PATH = ROOT_DIR / ".cursor/assets/photo.jpg"

def get_base64_image(path):
    if path.exists():
        with open(path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return ""

def p_wrap(text, style):
    return Paragraph(str(text), style)

def create_pdf_summary():
    """Generate professional PDF summary using reportlab"""
    output_path = DELIVERABLES_DIR / "report_summary.pdf"
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor(PRIMARY_COLOR),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor(SECONDARY_COLOR),
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor(PRIMARY_COLOR),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        leading=16,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )
    
    bold_body = ParagraphStyle('BoldBody', parent=body_style, fontName='Helvetica-Bold')
    
    elements = []
    
    # 1. Title Page / Header
    elements.append(Spacer(1, 1*inch))
    elements.append(Paragraph(f"📊 {ANALYSIS_TITLE}", title_style))
    elements.append(Paragraph("Characterizing the users and segments reporting product issues", subtitle_style))
    elements.append(Spacer(1, 0.5 * inch))
    
    # Metadata Table
    meta_data = [
        [p_wrap("<b>Analysis Period:</b>", bold_body), p_wrap("January 2026", body_style)],
        [p_wrap("<b>Generated:</b>", bold_body), p_wrap(datetime.now().strftime('%B %d, %Y'), body_style)],
        [p_wrap("<b>Analyst:</b>", bold_body), p_wrap(ANALYST_NAME, body_style)],
        [p_wrap("<b>Data Source:</b>", bold_body), p_wrap("Supabase (support_tickets, accounts, users)", body_style)],
    ]
    meta_table = Table(meta_data, colWidths=[2*inch, 3*inch])
    meta_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 0.5 * inch))
    
    # 2. Executive Summary
    elements.append(Paragraph("Executive Summary", heading_style))
    summary_text = (
        "This analysis investigates the characteristics of users and accounts reporting bugs. "
        "We found that <b>Pro tier accounts</b> in <b>EdTech and MarTech</b> industries are the primary reporters. "
        "These users are highly engaged 'Power Users' triggering 15% more events than average. "
        "Critically, <b>54% of bug reports originate from Admins</b>, indicating friction in core configuration workflows."
    )
    elements.append(Paragraph(summary_text, body_style))
    
    # 3. Key Metrics Table
    elements.append(Paragraph("Key Findings by Plan", heading_style))
    with open(DATA_DIR / "bug_tickets_by_plan.json", "r") as f:
        plan_data = json.load(f)
    
    table_data = [[p_wrap("<b>Plan Tier</b>", bold_body), p_wrap("<b>Bug Tickets</b>", bold_body), p_wrap("<b>Bugs per Account</b>", bold_body)]]
    for row in plan_data:
        table_data.append([
            p_wrap(row['plan'].capitalize(), body_style),
            p_wrap(row['bug_ticket_count'], body_style),
            p_wrap(f"<b>{row['bugs_per_account']}</b>", body_style)
        ])
    
    t = Table(table_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(PRIMARY_COLOR)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(t)
    
    # 4. Recommendations
    elements.append(PageBreak())
    elements.append(Paragraph("Recommendations", heading_style))
    
    rec_data = [
        [p_wrap("<b>Action</b>", bold_body), p_wrap("<b>Expected Impact</b>", bold_body)],
        [p_wrap("Audit EdTech/MarTech feature workflows", body_style), p_wrap("High - Reduce industry friction", body_style)],
        [p_wrap("Admin UI/UX Polish", body_style), p_wrap("High - Improve renewal sentiment", body_style)],
        [p_wrap("Power User Beta Program", body_style), p_wrap("Medium - Catch bugs before release", body_style)]
    ]
    
    rt = Table(rec_data, colWidths=[3*inch, 3*inch])
    rt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(SUCCESS_COLOR)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(rt)
    
    # Footer
    elements.append(Spacer(1, 4 * inch))
    elements.append(Paragraph(FOOTER_TEXT, ParagraphStyle('Footer', parent=body_style, alignment=TA_CENTER, textColor=colors.grey, fontSize=9)))
    
    doc.build(elements)
    print(f"PDF summary generated: {output_path}")

def generate_html_reports():
    """Generate both static and interactive HTML reports with consistent branding"""
    profile_b64 = get_base64_image(PHOTO_PATH)
    
    # Load data
    with open(DATA_DIR / "bug_tickets_by_plan.json", "r") as f: plan_data = json.load(f)
    with open(DATA_DIR / "bug_tickets_by_industry.json", "r") as f: industry_data = json.load(f)
    with open(DATA_DIR / "bug_tickets_by_role.json", "r") as f: role_data = json.load(f)
    with open(DATA_DIR / "top_bug_reporters.json", "r") as f: top_reporters = json.load(f)
    with open(DATA_DIR / "engagement_reporters_vs_others.json", "r") as f: engagement_data = json.load(f)

    def get_html_content(is_interactive=False):
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{ANALYSIS_TITLE} | {ANALYST_NAME}</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    {f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">' if is_interactive else ''}
    {f'<link rel="stylesheet" href="https://cdn.datatables.net/1.13.7/css/dataTables.bootstrap5.min.css">' if is_interactive else ''}
    <style>
    :root {{
        --color-primary: {PRIMARY_COLOR};
        --color-primary-dark: {PRIMARY_DARK};
        --color-secondary: {SECONDARY_COLOR};
        --color-bg: #F8FAFC;
        --color-surface: #FFFFFF;
        --color-text: #1E293B;
        --color-text-secondary: #64748B;
        --color-border: #E2E8F0;
        --color-success: {SUCCESS_COLOR};
        --color-warning: {WARNING_COLOR};
        --color-error: {ERROR_COLOR};
        --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

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
        overflow: hidden;
    }}

    .report-header {{
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
        color: white;
        padding: 2.5rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }}

    .report-header img.profile {{
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 3px solid rgba(255,255,255,0.3);
        object-fit: cover;
    }}

    .header-content h1 {{
        font-size: 2rem;
        margin: 0;
        font-weight: 700;
    }}

    .header-content p {{
        margin: 0.25rem 0 0 0;
        opacity: 0.9;
        font-size: 1rem;
    }}

    .section {{
        padding: 2.5rem;
        border-bottom: 1px solid var(--color-border);
    }}

    .section-title {{
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--color-primary);
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--color-border);
    }}

    .executive-summary {{
        background: linear-gradient(135deg, #EFF6FF 0%, #F0F9FF 100%);
        border-left: 4px solid var(--color-primary);
        padding: 1.5rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 2rem;
    }}

    .recommendations {{
        background: linear-gradient(135deg, #ECFDF5 0%, #F0FDFA 100%);
        border-left: 4px solid var(--color-success);
        padding: 1.5rem;
        border-radius: 0 8px 8px 0;
        margin-top: 2rem;
    }}

    .metrics-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }}

    .metric-card {{
        background: white;
        border: 1px solid var(--color-border);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}

    .metric-card .value {{ 
        font-size: 2.25rem; 
        font-weight: 700; 
        color: var(--color-primary);
        margin-bottom: 0.5rem;
    }}
    
    .metric-card .label {{
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--color-text-secondary);
        font-weight: 600;
    }}

    .chart-container {{
        border: 1px solid var(--color-border);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 2rem 0;
        background: white;
    }}

    .chart {{
        width: 100%;
        height: 400px;
    }}

    .report-footer {{
        background: var(--color-bg);
        padding: 2.5rem;
        text-align: center;
        border-top: 1px solid var(--color-border);
        font-size: 0.875rem;
        color: var(--color-text-secondary);
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 1.5rem 0;
    }}

    table th {{
        background: var(--color-bg);
        padding: 1rem;
        text-align: left;
        font-weight: 600;
        border-bottom: 2px solid var(--color-border);
    }}

    table td {{
        padding: 1rem;
        border-bottom: 1px solid var(--color-border);
    }}
    </style>
</head>
<body>
    <div class="report-container">
        <div class="report-header">
            <img src="{profile_b64}" alt="Nimrod Fisher" class="profile">
            <div class="header-content">
                <h1>{ANALYSIS_TITLE}</h1>
                <p>Generated by {ANALYST_NAME} • {datetime.now().strftime('%B %d, %Y')}</p>
            </div>
        </div>

        <div class="section">
            <div class="executive-summary">
                <h2 style="font-size: 1.25rem; margin-bottom: 0.5rem; color: var(--color-primary);">Executive Summary</h2>
                <p>Our analysis reveals that <strong>Pro tier accounts</strong> in the <strong>EdTech and MarTech</strong> industries are the primary discovery point for product bugs. These reporters are <strong>highly engaged Power Users</strong> (triggering 15% more events than average). Critically, <strong>54% of all bug tickets originate from Admins</strong>, highlighting issues in high-value setup and management workflows.</p>
            </div>

            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="value">54%</div>
                    <div class="label">Admin Reported</div>
                </div>
                <div class="metric-card">
                    <div class="value">0.80</div>
                    <div class="label">Max Bugs/Account</div>
                </div>
                <div class="metric-card">
                    <div class="value">+15%</div>
                    <div class="label">Engagement Lift</div>
                </div>
            </div>

            <h2 class="section-title">Analysis Findings</h2>
            
            <div class="chart-container">
                <div id="plan-chart" class="chart"></div>
            </div>

            <div class="chart-container">
                <div id="industry-chart" class="chart"></div>
            </div>

            <h2 class="section-title">Data Explorer</h2>
            <table id="dataTable" class="table">
                <thead>
                    <tr><th>Account Name</th><th>Plan</th><th>Industry</th><th>Bug Tickets</th></tr>
                </thead>
                <tbody>
                    {''.join([f"<tr><td>{r['account_name']}</td><td>{r['plan'].capitalize()}</td><td>{r['industry']}</td><td>{r['bug_ticket_count']}</td></tr>" for r in top_reporters])}
                </tbody>
            </table>

            <div class="recommendations">
                <h2 style="font-size: 1.25rem; margin-bottom: 0.5rem; color: var(--color-success);">Actionable Recommendations</h2>
                <ul style="margin-bottom: 0;">
                    <li><strong>Audit EdTech/MarTech workflows:</strong> Conduct targeted QA on industry-specific features.</li>
                    <li><strong>Admin UI/UX Polish:</strong> Improve friction points in account setup and user management.</li>
                    <li><strong>Beta Program:</strong> Recruit vocal Pro tier users for early feature validation.</li>
                </ul>
            </div>
        </div>

        <div class="report-footer">
            <p>{FOOTER_TEXT}</p>
            <p style="font-size: 0.75rem; margin-top: 0.5rem;">Confidential Analysis • {WEBSITE}</p>
        </div>
    </div>

    <script>
        const planChart = echarts.init(document.getElementById('plan-chart'));
        planChart.setOption({{
            title: {{ text: 'Bug Tickets by Plan Tier', left: 'center', textStyle: {{ fontFamily: 'Inter' }} }},
            tooltip: {{ trigger: 'axis' }},
            xAxis: {{ type: 'category', data: {json.dumps([r['plan'].capitalize() for r in plan_data])} }},
            yAxis: {{ type: 'value' }},
            series: [{{
                data: {json.dumps([r['bug_ticket_count'] for r in plan_data])},
                type: 'bar',
                itemStyle: {{ color: '{PRIMARY_COLOR}' }},
                label: {{ show: true, position: 'top' }}
            }}]
        }});

        const industryChart = echarts.init(document.getElementById('industry-chart'));
        industryChart.setOption({{
            title: {{ text: 'Bug Distribution by Industry', left: 'center' }},
            tooltip: {{ trigger: 'item' }},
            legend: {{ orient: 'vertical', left: 'left', top: 'center' }},
            series: [{{
                type: 'pie',
                radius: ['40%', '70%'],
                center: ['60%', '50%'],
                data: {json.dumps([{"name": r['industry'], "value": r['bug_ticket_count']} for r in industry_data if r['bug_ticket_count'] > 0])},
                emphasis: {{ itemStyle: {{ shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' }} }}
            }}]
        }});

        {'$("#dataTable").DataTable();' if is_interactive else ''}
    </script>
    {f'<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>' if is_interactive else ''}
    {f'<script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>' if is_interactive else ''}
    {f'<script src="https://cdn.datatables.net/1.13.7/js/dataTables.bootstrap5.min.js"></script>' if is_interactive else ''}
</body>
</html>"""

    # Write Static Report
    with open(DELIVERABLES_DIR / "report.html", "w", encoding="utf-8") as f:
        f.write(get_html_content(is_interactive=False))
    
    # Write Interactive Report
    with open(DELIVERABLES_DIR / "report_interactive.html", "w", encoding="utf-8") as f:
        f.write(get_html_content(is_interactive=True))
    
    print(f"HTML reports generated in {DELIVERABLES_DIR}")

if __name__ == "__main__":
    DELIVERABLES_DIR.mkdir(parents=True, exist_ok=True)
    create_pdf_summary()
    generate_html_reports()


"""
Generate PDF Summary Report for ARR Historical Analysis
Uses reportlab to create a professional PDF summary
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def create_pdf_summary():
    """Generate PDF summary report"""
    
    # Output path
    output_path = "deliverables/report_summary.pdf"
    
    # Create PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Container for elements
    elements = []
    
    # Get stylesheet
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#0EA5E9'),
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2563EB'),
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
    
    # Title Page
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph("📊 ARR Historical Analysis", title_style))
    elements.append(Paragraph("Annual Recurring Revenue by Plan Tier", subtitle_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("June 2024 - December 2025", subtitle_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # Metadata
    meta_data = [
        ["Analysis Period:", "19 Months (June 2024 - December 2025)"],
        ["Generated:", datetime.now().strftime('%B %d, %Y')],
        ["Analyst:", "Nimrod Fisher | AI Analytics Hub"],
        ["Data Source:", "Supabase (subscriptions + accounts)"],
    ]
    
    meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
    meta_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2563EB')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(meta_table)
    
    elements.append(PageBreak())
    
    # Executive Summary
    elements.append(Paragraph("Executive Summary", heading_style))
    
    summary_text = """
    Our Annual Recurring Revenue (ARR) has grown dramatically from <b>$8,064</b> in June 2024 to 
    <b>$111,864</b> in December 2025—a remarkable <b>1,287% increase</b> over 19 months. However, 
    this impressive growth trajectory has plateaued since March 2025, with ARR declining 5% from its 
    peak of $117,336 and remaining essentially flat for the past six months.
    <br/><br/>
    All three plan tiers (Free, Pro, Enterprise) now contribute roughly equally to revenue (~$37K each), 
    indicating excellent diversification but also revealing that Enterprise customers have experienced 
    higher churn rates than other tiers. The business has successfully scaled from 8 subscriptions to 88, 
    but growth has stalled and requires immediate strategic attention.
    """
    
    elements.append(Paragraph(summary_text, body_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Key Metrics Table
    elements.append(Paragraph("Key Metrics at a Glance", heading_style))
    
    # Helper to wrap text in Paragraph for table cells
    def p_wrap(text, style=body_style):
        return Paragraph(text, style)

    metrics_data = [
        [p_wrap('<b>Metric</b>'), p_wrap('<b>Value</b>'), p_wrap('<b>Change</b>')],
        [p_wrap('Current Total ARR'), p_wrap('$111,864'), p_wrap('+$103,800 from Jun \'24')],
        [p_wrap('Total Growth'), p_wrap('+1,287%'), p_wrap('19-month period')],
        [p_wrap('Peak ARR'), p_wrap('$117,336'), p_wrap('March 2025')],
        [p_wrap('Active Subscriptions'), p_wrap('88'), p_wrap('29 Free, 27 Pro, 32 Enterprise')],
        [p_wrap('Current MoM Growth'), p_wrap('0.0%'), p_wrap('Flat for 6 months')],
    ]
    
    metrics_table = Table(metrics_data, colWidths=[2.3*inch, 1.8*inch, 2.5*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 11),
        ('FONT', (0, 1), (-1, -1), 'Helvetica', 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(metrics_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # ARR by Plan Table
    elements.append(Paragraph("ARR Growth by Plan Tier", heading_style))
    
    plan_data = [
        [p_wrap('<b>Plan</b>'), p_wrap('<b>Jun 2024 ARR</b>'), p_wrap('<b>Dec 2025 ARR</b>'), p_wrap('<b>Growth</b>'), p_wrap('<b>% Growth</b>'), p_wrap('<b>Peak ARR</b>')],
        [p_wrap('Free'), p_wrap('$1,644'), p_wrap('$37,896'), p_wrap('+$36,252'), p_wrap('+2,205%'), p_wrap('$38,196')],
        [p_wrap('Pro'), p_wrap('$3,684'), p_wrap('$37,476'), p_wrap('+$33,792'), p_wrap('+917%'), p_wrap('$37,476')],
        [p_wrap('Enterprise'), p_wrap('$2,736'), p_wrap('$36,492'), p_wrap('+$33,756'), p_wrap('+1,234%'), p_wrap('$43,308')],
        [p_wrap('<b>Total</b>'), p_wrap('<b>$8,064</b>'), p_wrap('<b>$111,864</b>'), p_wrap('<b>+$103,800</b>'), p_wrap('<b>+1,287%</b>'), p_wrap('<b>$117,336</b>')],
    ]
    
    plan_table = Table(plan_data, colWidths=[1.2*inch, 1.1*inch, 1.1*inch, 1.1*inch, 1*inch, 1.1*inch])
    plan_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
        ('FONT', (0, 1), (-1, -2), 'Helvetica', 9),
        ('FONT', (0, -1), (-1, -1), 'Helvetica-Bold', 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ffeaa7')),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(plan_table)
    
    elements.append(PageBreak())
    
    # Key Findings
    elements.append(Paragraph("Key Findings", heading_style))
    
    finding1 = """
    <b>Finding 1: Explosive Growth Followed by Plateau</b><br/>
    ARR grew 1,387% in the first 6 months (June-December 2024), continued growing through March 2025 
    to peak at $117,336, but has since declined 5% and remained flat for 6 months. The current stagnation 
    suggests the business has hit a growth ceiling where new subscriptions only replace canceled ones.
    """
    elements.append(Paragraph(finding1, body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    finding2 = """
    <b>Finding 2: Balanced Revenue Distribution</b><br/>
    Revenue is remarkably balanced across all three plan tiers (Free: 33.9%, Pro: 33.5%, Enterprise: 32.6%). 
    While this provides excellent diversification, it may indicate pricing inefficiencies, as higher tiers 
    should typically contribute disproportionately more revenue per subscription.
    """
    elements.append(Paragraph(finding2, body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    finding3 = """
    <b>Finding 3: Enterprise Tier Volatility ⚠️</b><br/>
    The Enterprise plan peaked at $43,308 in March 2025 but declined 16% to $36,492 by June 2025. 
    This represents a loss of $6,816 in high-value ARR. At $1,258 average monthly price per Enterprise 
    subscription, losing just 2-3 accounts represents $30K-$45K in lost annual revenue.
    """
    elements.append(Paragraph(finding3, body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    finding4 = """
    <b>Finding 4: April 2025 Synchronized Decline</b><br/>
    April 2025 marked the first month where all three plan tiers experienced simultaneous ARR decline 
    (Enterprise: -5.8%, Free: -9.0%, Pro: -2.6%). This synchronized drop points to a systematic issue 
    rather than plan-specific problems—possibly a market shift, competitive pressure, product issue, 
    or service disruption.
    """
    elements.append(Paragraph(finding4, body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    finding5 = """
    <b>Finding 5: Free Plan Leading Growth</b><br/>
    The Free plan grew 2,205%, significantly outpacing Pro (917%) and Enterprise (1,234%). While Free 
    tier growth is positive, it may indicate challenges in upselling to higher-value tiers or suggest 
    product-market fit is strongest at the lower price point, which limits long-term expansion potential.
    """
    elements.append(Paragraph(finding5, body_style))
    
    elements.append(PageBreak())
    
    # Recommendations
    elements.append(Paragraph("Recommendations", heading_style))
    
    critical_box = """
    <b><font color='#721c24'>🔴 CRITICAL: Immediate Actions (0-30 days)</font></b><br/>
    1. <b>Investigate April 2025 Decline:</b> Conduct retrospective analysis of what changed in April 2025 
       (product updates, pricing changes, support issues, market events)<br/>
    2. <b>Enterprise Retention Program:</b> Contact all 29 Enterprise accounts, conduct health checks, 
       identify churn risks<br/>
    3. <b>Churn Analysis:</b> Deep-dive into 32 canceled subscriptions from March-May 2025, categorize 
       reasons, identify patterns
    """
    elements.append(Paragraph(critical_box, body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    short_term = """
    <b><font color='#856404'>🟡 HIGH PRIORITY: Short-term (1-3 months)</font></b><br/>
    1. <b>Win-Back Campaign:</b> Re-engage churned Enterprise accounts (potential $15K-$25K ARR recovery)<br/>
    2. <b>Upsell Strategy:</b> Build Free→Pro upgrade playbook (25% conversion could add $15K-$20K ARR)<br/>
    3. <b>Pricing Review:</b> Conduct pricing analysis to ensure tiers are correctly positioned<br/>
    4. <b>Early Warning System:</b> Build automated alerts for usage drops and payment failures
    """
    elements.append(Paragraph(short_term, body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    long_term = """
    <b><font color='#155724'>🟢 STRATEGIC: Long-term (3-6 months)</font></b><br/>
    1. <b>NRR Tracking:</b> Implement cohort-based Net Revenue Retention analysis<br/>
    2. <b>Enterprise Expansion:</b> Focus on adding new Enterprise customers (potential +30-50% ARR)<br/>
    3. <b>Product-Market Fit:</b> Research why Enterprise tier is volatile—product-value alignment?<br/>
    4. <b>Expansion Revenue:</b> Create account expansion playbook for existing customers
    """
    elements.append(Paragraph(long_term, body_style))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Expected Impact Table
    elements.append(Paragraph("Expected Impact of Recommendations", heading_style))
    
    impact_data = [
        [p_wrap('<b>Initiative</b>'), p_wrap('<b>Timeframe</b>'), p_wrap('<b>Expected Impact</b>')],
        [p_wrap('Churn Prevention Program'), p_wrap('1-3 months'), p_wrap('20-30% churn reduction')],
        [p_wrap('Win-Back Campaign'), p_wrap('1-3 months'), p_wrap('$15K-$25K ARR recovery')],
        [p_wrap('Free→Pro Upsell'), p_wrap('2-4 months'), p_wrap('$15K-$20K additional ARR')],
        [p_wrap('Enterprise Expansion'), p_wrap('3-6 months'), p_wrap('$35K-$55K ARR growth')],
        [p_wrap('<b>Total Potential</b>'), p_wrap('<b>6 months</b>'), p_wrap('<b>$65K-$100K ARR increase</b>')],
    ]
    
    impact_table = Table(impact_data, colWidths=[2.2*inch, 1.8*inch, 2.6*inch])
    impact_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
        ('FONT', (0, 1), (-1, -2), 'Helvetica', 9),
        ('FONT', (0, -1), (-1, -1), 'Helvetica-Bold', 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d4edda')),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(impact_table)
    
    elements.append(PageBreak())
    
    # Methodology
    elements.append(Paragraph("Methodology", heading_style))
    
    methodology_text = """
    <b>Data Sources:</b> Supabase database (subscriptions + accounts tables)<br/>
    <b>Analysis Period:</b> June 2024 - December 2025 (19 months)<br/>
    <b>Query Technique:</b> Time-series analysis using month series CROSS JOIN<br/>
    <b>Validation:</b> 11 data quality checks performed, all passed<br/>
    <b>Active Definition:</b> A subscription is considered "active" in a month if started_at ≤ month_end 
    AND (canceled_at IS NULL OR canceled_at > month_end)<br/>
    <b>ARR Calculation:</b> monthly_price × 12 for all active subscriptions<br/>
    <b>Tools:</b> PostgreSQL/Supabase SQL, Python Analysis Framework, ECharts visualization
    """
    elements.append(Paragraph(methodology_text, body_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Data Quality
    elements.append(Paragraph("Data Quality Summary", heading_style))
    
    quality_data = [
        [p_wrap('<b>Quality Dimension</b>'), p_wrap('<b>Score</b>'), p_wrap('<b>Notes</b>')],
        [p_wrap('Completeness'), p_wrap('5/5'), p_wrap('No missing values in required fields')],
        [p_wrap('Accuracy'), p_wrap('5/5'), p_wrap('All values within expected ranges')],
        [p_wrap('Consistency'), p_wrap('5/5'), p_wrap('Date ranges valid, foreign keys intact')],
        [p_wrap('Timeliness'), p_wrap('5/5'), p_wrap('Data complete through current month')],
        [p_wrap('<b>Overall</b>'), p_wrap('<b>5/5</b>'), p_wrap('<b>Excellent data quality</b>')],
    ]
    
    quality_table = Table(quality_data, colWidths=[2.2*inch, 1.2*inch, 3.2*inch])
    quality_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (2, -1), 'LEFT'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
        ('FONT', (0, 1), (-1, -2), 'Helvetica', 9),
        ('FONT', (0, -1), (-1, -1), 'Helvetica-Bold', 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d4edda')),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(quality_table)
    
    # Footer
    elements.append(Spacer(1, 0.5*inch))
    footer_text = """
    <br/><br/>
    <b>For detailed analysis and interactive visualizations, please refer to:</b><br/>
    • Interactive Dashboard (report_interactive.html)<br/>
    • Static HTML Report (report.html)<br/>
    • Complete EDA Report (eda/eda_report.md)<br/>
    • Analysis Flow Documentation (analysis_flow.md)<br/>
    • Conclusions Document (conclusions/conclusions.md)
    """
    elements.append(Paragraph(footer_text, body_style))
    
    # Build PDF
    doc.build(elements)
    
    print(f"[SUCCESS] PDF summary report generated: {output_path}")
    print(f"  File size: {os.path.getsize(output_path) / 1024:.1f} KB")
    return output_path

if __name__ == "__main__":
    print("="*80)
    print("GENERATING PDF SUMMARY REPORT")
    print("="*80)
    
    try:
        output_file = create_pdf_summary()
        print("\n" + "="*80)
        print("PDF GENERATION COMPLETE")
        print("="*80)
        print(f"\nOpen '{output_file}' to view the executive summary.")
    except Exception as e:
        print(f"\n[ERROR] Error generating PDF: {e}")
        print("\nTo install required library, run: pip install reportlab")

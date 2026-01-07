"""
================================================================================
Bug Reporter Characterization Analysis - PDF Report Generator
================================================================================
Author: AI Analytics Team
Created: 2026-01-07
Description: Generates a professional PDF summary report using ReportLab
================================================================================
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime

# Custom color palette (matching HTML reports)
PRIMARY = colors.HexColor('#2563EB')
SECONDARY = colors.HexColor('#0EA5E9')
SUCCESS = colors.HexColor('#10B981')
WARNING = colors.HexColor('#FF9800')
ERROR = colors.HexColor('#EF4444')
ACCENT = colors.HexColor('#667eea')

def p_wrap(text, style):
    """Wrapper function to convert text to Paragraph (MANDATORY for table cells)"""
    return Paragraph(text, style)

def create_pdf_report(output_path):
    """Generate the complete PDF report"""
    
    # Initialize document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Container for PDF elements
    story = []
    
    # Custom styles
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=PRIMARY,
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Subtitle style
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=SECONDARY,
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    # Heading style
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=PRIMARY,
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Body style
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )
    
    # Bold body style
    bold_style = ParagraphStyle(
        'BoldBody',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    # Small text style
    small_style = ParagraphStyle(
        'SmallText',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    
    # ============================================================
    # COVER PAGE
    # ============================================================
    story.append(Spacer(1, 0.5*inch))
    
    story.append(Paragraph("🔍 Bug Reporter Characterization Analysis", title_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Understanding What Drives Product Bug Reporting", subtitle_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Metadata table
    meta_data = [
        [p_wrap('<b>Analysis Date:</b>', body_style), p_wrap('January 7, 2026', body_style)],
        [p_wrap('<b>Analyst:</b>', body_style), p_wrap('AI Analytics Team', body_style)],
        [p_wrap('<b>Data Period:</b>', body_style), p_wrap('December 2024 - June 2025', body_style)],
        [p_wrap('<b>Analysis Type:</b>', body_style), p_wrap('Cohort Characterization & Behavioral Analysis', body_style)],
    ]
    
    meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
    meta_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(meta_table)
    story.append(Spacer(1, 0.5*inch))
    
    # ============================================================
    # EXECUTIVE SUMMARY
    # ============================================================
    story.append(Paragraph("Executive Summary", heading_style))
    
    exec_summary = """This analysis reveals that <b>bug reporting is a positive signal of product engagement</b>, 
    not merely a quality issue. Our findings show that bug reporters exhibit <b>15.5% higher user-level engagement</b> 
    and <b>81.8% higher account-level engagement</b> compared to non-reporters. Admin roles dominate bug reporting 
    (52.4% vs 34% baseline), and most bugs are discovered during the critical <b>first 1-2 weeks of onboarding</b> 
    (median 6 days). Notably, <b>50% of trial accounts and 80% of enterprise trials</b> report bugs—the highest rates 
    of any segment—indicating active product evaluation. These insights suggest bug reporting should be tracked as an 
    engagement metric and that onboarding quality improvements could significantly reduce initial friction."""
    
    story.append(Paragraph(exec_summary, body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # ============================================================
    # KEY METRICS TABLE
    # ============================================================
    story.append(Paragraph("Key Metrics at a Glance", heading_style))
    
    metrics_data = [
        [p_wrap('<b>Metric</b>', bold_style), 
         p_wrap('<b>Value</b>', bold_style), 
         p_wrap('<b>Significance</b>', bold_style)],
        
        [p_wrap('Bug Reporters', body_style), 
         p_wrap('<b>10.5%</b><br/>(21 of 200 users)', body_style), 
         p_wrap('Small but active cohort', body_style)],
        
        [p_wrap('User-Level Engagement Lift', body_style), 
         p_wrap('<b><font color="#10B981">+15.5%</font></b><br/>(11.14 vs 9.64 avg events)', body_style), 
         p_wrap('<font color="#10B981"><b>Positive correlation</b></font>', body_style)],
        
        [p_wrap('Account-Level Engagement Lift', body_style), 
         p_wrap('<b><font color="#10B981">+81.8%</font></b><br/>(378.5 vs 208.2 avg events)', body_style), 
         p_wrap('<font color="#10B981"><b>Very strong correlation</b></font>', body_style)],
        
        [p_wrap('Admin Role Dominance', body_style), 
         p_wrap('<b>52.4%</b><br/>(vs 34% baseline)', body_style), 
         p_wrap('Admins over-represented by 53.6%', body_style)],
        
        [p_wrap('Median Time to First Bug', body_style), 
         p_wrap('<b><font color="#FF9800">6 days</font></b><br/>(onboarding period)', body_style), 
         p_wrap('<font color="#FF9800"><b>Critical window</b></font>', body_style)],
        
        [p_wrap('Trial Account Bug Rate', body_style), 
         p_wrap('<b><font color="#EF4444">50%</font></b><br/>(80% for Enterprise trials)', body_style), 
         p_wrap('<font color="#EF4444"><b>Highest rate</b></font>', body_style)],
    ]
    
    metrics_table = Table(metrics_data, colWidths=[2.5*inch, 2.2*inch, 2*inch])
    metrics_table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Data rows
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        
        # Alternating row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    story.append(metrics_table)
    story.append(PageBreak())
    
    # ============================================================
    # KEY FINDINGS
    # ============================================================
    story.append(Paragraph("Key Findings", heading_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Finding 1
    story.append(Paragraph("<b>1. Bug Reporting = Engagement Signal</b>", bold_style))
    finding1 = """Bug reporters show significantly higher engagement: <b>+15.5% at the user level</b> and 
    <b>+81.8% at the account level</b>. Bug-reporting accounts have <b>53% higher engagement intensity</b> 
    (89 vs 58.17 events per user). This pattern suggests that bug reporting is driven by product usage—
    users who engage more with the product naturally encounter more edge cases and issues. <b>Recommendation:</b> 
    Track bug reporting rate as a positive engagement metric alongside traditional KPIs."""
    story.append(Paragraph(finding1, body_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Finding 2
    story.append(Paragraph("<b>2. Critical Onboarding Period (0-14 Days)</b>", bold_style))
    finding2 = """The <b>median time to first bug is 6 days</b> after signup (average 14 days), and 
    <b>95.24% of bug reporters only report ONE bug</b>. This reveals that bugs are discovered during initial 
    product exploration and onboarding, not through long-term usage. The one-time reporting pattern suggests 
    users either adapt to workarounds or the issues get resolved. <b>Recommendation:</b> Prioritize 
    onboarding flow QA, implement proactive support during days 1-14, and create guided tours to reduce friction."""
    story.append(Paragraph(finding2, body_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Finding 3
    story.append(Paragraph("<b>3. Trial Users Are Highly Active Bug Reporters</b>", bold_style))
    finding3 = """<b>50% of trial accounts (no subscription)</b> report bugs, with <b>80% for enterprise trials</b>—
    the highest rates of any customer segment. In contrast, low MRR paying customers report the fewest bugs (16.7%). 
    This U-shaped pattern indicates that trial users are actively evaluating the product and providing critical feedback, 
    while low-value customers may be less engaged or using simpler features. <b>Recommendation:</b> Fast-track bug fixes 
    for trial accounts, monitor trial-to-paid conversion correlation with bug reporting, and investigate low-MRR 
    customer engagement."""
    story.append(Paragraph(finding3, body_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Finding 4
    story.append(Paragraph("<b>4. Admin Users Drive Bug Discovery</b>", bold_style))
    finding4 = """<b>52.38% of bug reporters are admins</b> compared to a 34.08% baseline—an over-representation 
    of <b>+53.6%</b>. Conversely, viewers are under-represented (19.05% vs 35.20%). Admin users have broader 
    product access, use more features, and are more invested in product quality, leading to higher bug discovery 
    rates. <b>Recommendation:</b> Increase test coverage for admin-specific features, prioritize admin-reported bugs, 
    and consider admin-specific QA protocols."""
    story.append(Paragraph(finding4, body_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Finding 5
    story.append(Paragraph("<b>5. Industry Patterns: MarTech & HealthTech Complexity</b>", bold_style))
    finding5 = """<b>MarTech (25% vs 10%, +150%)</b> and <b>HealthTech (20% vs 10%, +100%)</b> accounts are 
    significantly over-represented among bug reporters, while <b>FinTech accounts show 0% bug reporting</b> despite 
    representing 20% of non-reporters. This suggests complex, feature-rich use cases in MarTech/HealthTech surface 
    more bugs, while FinTech may use simpler workflows, have higher tolerance, or encounter fewer issues. 
    <b>Recommendation:</b> Create industry-specific test scenarios for MarTech/HealthTech and investigate FinTech 
    usage patterns for best practices."""
    story.append(Paragraph(finding5, body_style))
    story.append(PageBreak())
    
    # ============================================================
    # RECOMMENDATIONS TABLE
    # ============================================================
    story.append(Paragraph("Actionable Recommendations", heading_style))
    story.append(Spacer(1, 0.1*inch))
    
    rec_data = [
        [p_wrap('<b>Priority</b>', bold_style), 
         p_wrap('<b>Action</b>', bold_style), 
         p_wrap('<b>Expected Impact</b>', bold_style)],
        
        [p_wrap('<font color="#EF4444"><b>HIGH</b></font>', body_style),
         p_wrap('<b>Improve Onboarding Experience (Days 1-14)</b><br/>'
                '• Focus testing on first-week user journeys<br/>'
                '• Add proactive support/chat during onboarding<br/>'
                '• Create guided tours for core features<br/>'
                '• Monitor onboarding completion metrics', body_style),
         p_wrap('Reduce bug discovery by <b>20-30%</b> in first 2 weeks; '
                'improve trial-to-paid conversion', body_style)],
        
        [p_wrap('<font color="#EF4444"><b>HIGH</b></font>', body_style),
         p_wrap('<b>Prioritize Trial User Bug Fixes</b><br/>'
                '• Fast-track bugs from no-subscription accounts<br/>'
                '• Create "trial-critical" bug severity tier<br/>'
                '• Monitor trial-to-paid correlation with bugs', body_style),
         p_wrap('Improve conversion rates by <b>5-10%</b>; '
                'capture high-value customers', body_style)],
        
        [p_wrap('<font color="#FF9800"><b>MEDIUM</b></font>', body_style),
         p_wrap('<b>Enhance Admin Feature Quality</b><br/>'
                '• Increase test coverage for admin features<br/>'
                '• Prioritize admin-reported bugs in sprint planning<br/>'
                '• Create admin-specific QA protocols', body_style),
         p_wrap('Reduce admin churn by <b>10-15%</b>; '
                'improve power user satisfaction', body_style)],
        
        [p_wrap('<font color="#FF9800"><b>MEDIUM</b></font>', body_style),
         p_wrap('<b>Industry-Specific Testing</b><br/>'
                '• Create MarTech/HealthTech test scenarios<br/>'
                '• Investigate FinTech usage patterns<br/>'
                '• Develop industry-specific documentation', body_style),
         p_wrap('Reduce industry-specific bugs by <b>15-25%</b>; '
                'improve product-market fit', body_style)],
        
        [p_wrap('<font color="#10B981"><b>LOW</b></font>', body_style),
         p_wrap('<b>Track Bug Reporting as Engagement Metric</b><br/>'
                '• Add bug reporting rate to dashboards<br/>'
                '• Correlate with retention and expansion<br/>'
                '• Create early-warning system for disengagement', body_style),
         p_wrap('Enable proactive retention; '
                'identify at-risk accounts earlier', body_style)],
    ]
    
    rec_table = Table(rec_data, colWidths=[0.8*inch, 3.7*inch, 2.2*inch])
    rec_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Data
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ('ALIGN', (1, 1), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    story.append(rec_table)
    story.append(Spacer(1, 0.3*inch))
    
    # ============================================================
    # METHODOLOGY
    # ============================================================
    story.append(Paragraph("Methodology", heading_style))
    
    methodology = """This analysis employed a <b>cohort comparison methodology</b> across four dimensions: 
    (1) <b>User-level characterization</b> comparing 21 bug reporters to 179 non-reporters on demographic 
    (role, tenure, plan tier) and behavioral (event volume, diversity) metrics; (2) <b>Account-level 
    characterization</b> comparing 20 bug-reporting accounts to 30 non-reporting accounts on organizational 
    metrics (industry, team size, event activity); (3) <b>Behavioral timing analysis</b> examining time to 
    first bug report, repeat behavior, and pre/post-bug event patterns; (4) <b>Customer value analysis</b> 
    segmenting accounts by MRR to identify bug reporting patterns by customer tier. Data was sourced from 
    production tables (users, accounts, events, support_tickets, subscriptions) covering December 2024 - 
    June 2025. All queries underwent validation checks for data quality, join integrity, and time-series 
    completeness before analysis."""
    
    story.append(Paragraph(methodology, body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # ============================================================
    # FOOTER
    # ============================================================
    story.append(Spacer(1, 0.5*inch))
    
    footer_line = "─" * 80
    story.append(Paragraph(footer_line, small_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>Nimrod Fisher | AI Analytics Hub</b>", 
                          ParagraphStyle('Footer', parent=small_style, fontSize=12, 
                                       textColor=PRIMARY, fontName='Helvetica-Bold')))
    story.append(Paragraph("Advanced Analytics & Data Intelligence Solutions", small_style))
    story.append(Paragraph(f"Report Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", small_style))
    
    # ============================================================
    # BUILD PDF
    # ============================================================
    doc.build(story)
    print(f"[SUCCESS] PDF report generated successfully: {output_path}")

if __name__ == "__main__":
    # Ensure deliverables folder exists
    from pathlib import Path
    Path("./deliverables").mkdir(exist_ok=True)
    
    # Use standardized filename in deliverables folder
    output_file = "deliverables/report_summary.pdf"
    create_pdf_report(output_file)


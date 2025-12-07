#!/usr/bin/env python3
"""
Research Report Generator
Generates a modern, tech-style PDF report with Claude's answer and Google search results
"""

import sys
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# Modern tech color scheme - Light background with blue accents
COLOR_PRIMARY = colors.HexColor('#1E40AF')  # Deep blue
COLOR_SECONDARY = colors.HexColor('#3B82F6')  # Bright blue
COLOR_ACCENT = colors.HexColor('#60A5FA')  # Light blue
COLOR_BG_LIGHT = colors.HexColor('#F8FAFC')  # Very light gray/blue
COLOR_TEXT_PRIMARY = colors.HexColor('#1E293B')  # Dark slate
COLOR_TEXT_SECONDARY = colors.HexColor('#475569')  # Medium slate
COLOR_BORDER = colors.HexColor('#E2E8F0')  # Light border

# Register Chinese fonts
def register_chinese_fonts():
    """Register Chinese fonts for PDF generation"""
    try:
        # Try to register STHeiti (Heiti SC) - macOS system font
        pdfmetrics.registerFont(TTFont('STHeiti', '/System/Library/Fonts/STHeiti Medium.ttc', subfontIndex=0))
        pdfmetrics.registerFont(TTFont('STHeiti-Bold', '/System/Library/Fonts/STHeiti Medium.ttc', subfontIndex=1))
        return 'STHeiti', 'STHeiti-Bold'
    except:
        try:
            # Fallback to Songti
            pdfmetrics.registerFont(TTFont('Songti', '/System/Library/Fonts/Supplemental/Songti.ttc', subfontIndex=0))
            return 'Songti', 'Songti'
        except:
            # If all fails, use Helvetica (won't display Chinese properly)
            print("Warning: Could not load Chinese fonts. Chinese characters may not display correctly.")
            return 'Helvetica', 'Helvetica-Bold'

# Register fonts at module level
FONT_NORMAL, FONT_BOLD = register_chinese_fonts()

def create_styles():
    """Create custom paragraph styles for the report"""
    styles = getSampleStyleSheet()

    # Main title style
    styles.add(ParagraphStyle(
        name='QuestionTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=COLOR_PRIMARY,
        spaceAfter=30,
        spaceBefore=10,
        leading=30,
        alignment=TA_LEFT,
        fontName=FONT_BOLD
    ))

    # Section header style
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=COLOR_PRIMARY,
        spaceAfter=12,
        spaceBefore=20,
        leading=20,
        fontName=FONT_BOLD,
        borderWidth=0,
        borderColor=COLOR_BORDER,
        borderPadding=5
    ))

    # Body text style
    styles.add(ParagraphStyle(
        name='ReportBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=COLOR_TEXT_PRIMARY,
        spaceAfter=12,
        leading=16,
        alignment=TA_LEFT,
        fontName=FONT_NORMAL
    ))

    # Link style
    styles.add(ParagraphStyle(
        name='ReportLink',
        parent=styles['Normal'],
        fontSize=10,
        textColor=COLOR_SECONDARY,
        spaceAfter=8,
        leading=14,
        fontName=FONT_NORMAL,
        underline=True
    ))

    # Source description style
    styles.add(ParagraphStyle(
        name='ReportSourceDesc',
        parent=styles['Normal'],
        fontSize=10,
        textColor=COLOR_TEXT_SECONDARY,
        spaceAfter=15,
        leading=14,
        fontName=FONT_NORMAL,
        leftIndent=20
    ))

    # Metadata style
    styles.add(ParagraphStyle(
        name='ReportMetadata',
        parent=styles['Normal'],
        fontSize=9,
        textColor=COLOR_TEXT_SECONDARY,
        spaceAfter=20,
        alignment=TA_LEFT,
        fontName=FONT_NORMAL
    ))

    return styles


def add_header(story, question, styles):
    """Add report header with question and metadata"""
    # Date
    date_text = f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}"
    story.append(Paragraph(date_text, styles['ReportMetadata']))

    # Question title with accent bar
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(question, styles['QuestionTitle']))

    # Divider line
    line_table = Table([['']], colWidths=[7*inch])
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 2, COLOR_ACCENT),
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_LIGHT),
    ]))
    story.append(line_table)
    story.append(Spacer(1, 0.2*inch))


def add_claude_answer(story, answer, styles):
    """Add Claude's answer section"""
    # Section header with background
    header_table = Table([['Claude AI Analysis']], colWidths=[7*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_LIGHT),
        ('TEXTCOLOR', (0, 0), (-1, -1), COLOR_PRIMARY),
        ('FONTNAME', (0, 0), (-1, -1), FONT_BOLD),
        ('FONTSIZE', (0, 0), (-1, -1), 16),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.15*inch))

    # Answer content
    paragraphs = answer.split('\n\n')
    for para in paragraphs:
        if para.strip():
            story.append(Paragraph(para.strip(), styles['ReportBody']))

    story.append(Spacer(1, 0.3*inch))


def add_search_results(story, results, styles):
    """Add Google search results section"""
    # Section header
    header_table = Table([['Top Search Results']], colWidths=[7*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_LIGHT),
        ('TEXTCOLOR', (0, 0), (-1, -1), COLOR_PRIMARY),
        ('FONTNAME', (0, 0), (-1, -1), FONT_BOLD),
        ('FONTSIZE', (0, 0), (-1, -1), 16),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.15*inch))

    # Search results
    for i, result in enumerate(results[:10], 1):
        # Result number and title
        title = result.get('title', 'No title')
        url = result.get('url', '#')
        description = result.get('description', 'No description available')

        # Create result card
        result_data = [[f"#{i}"]]
        result_table = Table(result_data, colWidths=[0.5*inch])
        result_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), COLOR_ACCENT),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), FONT_BOLD),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(result_table)
        story.append(Spacer(1, 0.05*inch))

        # Title
        story.append(Paragraph(f"<b>{title}</b>", styles['ReportBody']))

        # URL as clickable link
        link_text = f'<a href="{url}" color="{COLOR_SECONDARY}">{url}</a>'
        story.append(Paragraph(link_text, styles['ReportLink']))

        # Description
        story.append(Paragraph(description, styles['ReportSourceDesc']))

        story.append(Spacer(1, 0.15*inch))


def add_conclusion(story, conclusion, styles):
    """Add conclusion section"""
    # Section header
    header_table = Table([['Conclusion']], colWidths=[7*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_LIGHT),
        ('TEXTCOLOR', (0, 0), (-1, -1), COLOR_PRIMARY),
        ('FONTNAME', (0, 0), (-1, -1), FONT_BOLD),
        ('FONTSIZE', (0, 0), (-1, -1), 16),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.15*inch))

    # Conclusion content
    paragraphs = conclusion.split('\n\n')
    for para in paragraphs:
        if para.strip():
            story.append(Paragraph(para.strip(), styles['ReportBody']))


def generate_pdf(question, claude_answer, search_results, conclusion, output_path):
    """
    Generate the PDF report

    Args:
        question (str): The research question
        claude_answer (str): Claude's detailed answer
        search_results (list): List of dicts with 'title', 'url', 'description'
        conclusion (str): Final conclusion/summary
        output_path (str): Path to save the PDF
    """
    # Create PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Build story
    story = []
    styles = create_styles()

    # Add sections
    add_header(story, question, styles)
    add_claude_answer(story, claude_answer, styles)
    add_search_results(story, search_results, styles)
    add_conclusion(story, conclusion, styles)

    # Build PDF
    doc.build(story)
    print(f"✅ Report generated: {output_path}")


def main():
    """Main entry point for CLI usage"""
    if len(sys.argv) != 2:
        print("Usage: python generate_report.py <data.json>")
        print("\nExpected JSON format:")
        print(json.dumps({
            "question": "Your research question",
            "claude_answer": "Claude's detailed answer",
            "search_results": [
                {"title": "Result title", "url": "https://...", "description": "Brief description"}
            ],
            "conclusion": "Final summary and conclusion",
            "output_path": "path/to/output.pdf"
        }, indent=2))
        sys.exit(1)

    # Load data from JSON file
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Generate PDF
    generate_pdf(
        question=data['question'],
        claude_answer=data['claude_answer'],
        search_results=data['search_results'],
        conclusion=data['conclusion'],
        output_path=data.get('output_path', 'research_report.pdf')
    )


if __name__ == '__main__':
    main()

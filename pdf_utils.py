from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def create_study_pdf(student_name, summary):
    """
    Create a PDF from the generated study summary.

    Returns:
        bytes: PDF content
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="AI Study Notes Assistant",
        author="AI Study Notes Assistant",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=22,
        leading=28,
        alignment=TA_CENTER,
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        spaceBefore=10,
        spaceAfter=7,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10.5,
        leading=16,
        spaceAfter=6,
    )

    bullet_style = ParagraphStyle(
        "Bullet",
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
    )

    story = []

    # Title
    story.append(
        Paragraph(
            "AI Study Notes Assistant",
            title_style,
        )
    )

    story.append(
        Paragraph(
            f"Student: {student_name or 'Student'}",
            subtitle_style,
        )
    )

    # Small header table
    header_data = [
        [
            Paragraph("<b>Generated Study Notes</b>", body_style),
            Paragraph("AI-Powered Revision", body_style),
        ]
    ]

    header_table = Table(
        header_data,
        colWidths=[90 * mm, 70 * mm],
    )

    header_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.lightgrey),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(header_table)
    story.append(Spacer(1, 12))

    # Add summary
    if summary:
        lines = summary.splitlines()

        for line in lines:
            line = line.strip()

            if not line:
                story.append(Spacer(1, 5))
                continue

            # Remove emojis because standard PDF fonts may not support them.
            clean_line = remove_emojis(line)

            if not clean_line:
                continue

            # Headings
            if (
                clean_line.startswith("Topic:")
                or clean_line.startswith("Simple Explanation:")
                or clean_line.startswith("Important Points:")
                or clean_line.startswith("Important Concepts:")
                or clean_line.startswith("Key Terms:")
                or clean_line.startswith("Quick Revision:")
                or clean_line.startswith("Study Summary:")
                or clean_line.endswith(":")
            ):
                story.append(
                    Paragraph(
                        clean_line,
                        heading_style,
                    )
                )

            # Bullets
            elif line.startswith(("-", "•", "*")):
                clean_line = clean_line.lstrip("-•* ").strip()

                story.append(
                    Paragraph(
                        f"• {clean_line}",
                        bullet_style,
                    )
                )

            else:
                story.append(
                    Paragraph(
                        clean_line,
                        body_style,
                    )
                )

    else:
        story.append(
            Paragraph(
                "No study summary is available.",
                body_style,
            )
        )

    doc.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    buffer.seek(0)

    return buffer.getvalue()


def remove_emojis(text):
    """
    Remove characters that are not reliably supported
    by ReportLab's standard Helvetica font.
    """

    return text.encode(
        "ascii",
        "ignore",
    ).decode(
        "ascii"
    )


def add_page_number(canvas, document):
    """Add page number to each PDF page."""

    canvas.saveState()

    canvas.setFont(
        "Helvetica",
        8,
    )

    canvas.drawCentredString(
        A4[0] / 2,
        10 * mm,
        f"AI Study Notes Assistant - Page {document.page}",
    )

    canvas.restoreState()
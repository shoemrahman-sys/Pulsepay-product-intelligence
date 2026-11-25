
"""
PulsePay Product Analytics
Professional Business Report Generator

Generates an editable DOCX report and a PDF report
from validated analytical findings.

Does not independently invent or interpret findings.
"""

import json
from pathlib import Path
from datetime import datetime

from docx import Document
from docx.shared import Inches, Pt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

FINDINGS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ai_input"
    / "pulsepay_analysis_findings.json"
)

REPORT_DIR = PROJECT_ROOT / "reports" / "generated"


def load_findings():

    if not FINDINGS_FILE.exists():
        raise FileNotFoundError(
            "Validated findings file is missing: "
            f"{FINDINGS_FILE}"
        )

    with FINDINGS_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        findings = json.load(file)

    required_fields = [
        "project_title",
        "executive_summary",
        "sections",
        "recommendations",
    ]

    for field in required_fields:
        if field not in findings:
            raise ValueError(
                f"Required report field missing: {field}"
            )

    return findings


def create_docx(findings):

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    document = Document()

    document.add_heading(
        findings["project_title"],
        level=0
    )

    document.add_paragraph(
        "Product Analytics Business Case Study"
    )

    document.add_paragraph(
        f"Generated: {datetime.now():%d %B %Y}"
    )

    document.add_heading(
        "Executive Summary",
        level=1
    )

    document.add_paragraph(
        findings["executive_summary"]
    )

    for section in findings["sections"]:

        document.add_heading(
            section["title"],
            level=1
        )

        document.add_paragraph(
            section["content"]
        )

    document.add_heading(
        "Business Recommendations",
        level=1
    )

    for recommendation in findings["recommendations"]:

        document.add_paragraph(
            recommendation,
            style="List Bullet"
        )

    document.add_heading(
        "Analytical Limitations",
        level=1
    )

    for limitation in findings.get(
        "limitations",
        []
    ):

        document.add_paragraph(
            limitation,
            style="List Bullet"
        )

    output_file = (
        REPORT_DIR / "PulsePay_Product_Analytics_Report.docx"
    )

    document.save(output_file)

    return output_file


def create_pdf(findings):

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        REPORT_DIR / "PulsePay_Product_Analytics_Report.pdf"
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=22,
        leading=28,
        spaceAfter=20,
    )

    story = []

    story.append(
        Paragraph(
            findings["project_title"],
            title_style
        )
    )

    story.append(
        Paragraph(
            "Product Analytics Business Case Study",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 0.3 * inch)
    )

    story.append(
        Paragraph(
            "Executive Summary",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            findings["executive_summary"],
            styles["BodyText"]
        )
    )

    for section in findings["sections"]:

        story.append(
            Spacer(1, 0.2 * inch)
        )

        story.append(
            Paragraph(
                section["title"],
                styles["Heading1"]
            )
        )

        story.append(
            Paragraph(
                section["content"],
                styles["BodyText"]
            )
        )

    story.append(
        Spacer(1, 0.2 * inch)
    )

    story.append(
        Paragraph(
            "Business Recommendations",
            styles["Heading1"]
        )
    )

    for recommendation in findings["recommendations"]:

        story.append(
            Paragraph(
                f"&bull; {recommendation}",
                styles["BodyText"]
            )
        )

    story.append(
        Paragraph(
            "Analytical Limitations",
            styles["Heading1"]
        )
    )

    for limitation in findings.get(
        "limitations",
        []
    ):

        story.append(
            Paragraph(
                f"&bull; {limitation}",
                styles["BodyText"]
            )
        )

    pdf = SimpleDocTemplate(
        str(output_file),
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
    )

    pdf.build(story)

    return output_file


def generate_report():

    findings = load_findings()

    docx_file = create_docx(findings)
    pdf_file = create_pdf(findings)

    print("\n[PASS] Business report generated.")
    print(f"[INFO] DOCX: {docx_file}")
    print(f"[INFO] PDF: {pdf_file}")

    return True

"""
PulsePay Product Analytics
Professional Business Report Generator

Generates an editable DOCX report and a PDF report
from validated analytical findings.

Does not independently invent or interpret findings.
"""

import json
from pathlib import Path
from datetime import datetime

from docx import Document
from docx.shared import Inches, Pt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

FINDINGS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ai_input"
    / "pulsepay_analysis_findings.json"
)

REPORT_DIR = PROJECT_ROOT / "reports" / "generated"


def load_findings():

    if not FINDINGS_FILE.exists():
        raise FileNotFoundError(
            "Validated findings file is missing: "
            f"{FINDINGS_FILE}"
        )

    with FINDINGS_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        findings = json.load(file)

    required_fields = [
        "project_title",
        "executive_summary",
        "sections",
        "recommendations",
    ]

    for field in required_fields:
        if field not in findings:
            raise ValueError(
                f"Required report field missing: {field}"
            )

    return findings


def create_docx(findings):

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    document = Document()

    document.add_heading(
        findings["project_title"],
        level=0
    )

    document.add_paragraph(
        "Product Analytics Business Case Study"
    )

    document.add_paragraph(
        f"Generated: {datetime.now():%d %B %Y}"
    )

    document.add_heading(
        "Executive Summary",
        level=1
    )

    document.add_paragraph(
        findings["executive_summary"]
    )

    for section in findings["sections"]:

        document.add_heading(
            section["title"],
            level=1
        )

        document.add_paragraph(
            section["content"]
        )

    document.add_heading(
        "Business Recommendations",
        level=1
    )

    for recommendation in findings["recommendations"]:

        document.add_paragraph(
            recommendation,
            style="List Bullet"
        )

    document.add_heading(
        "Analytical Limitations",
        level=1
    )

    for limitation in findings.get(
        "limitations",
        []
    ):

        document.add_paragraph(
            limitation,
            style="List Bullet"
        )

    output_file = (
        REPORT_DIR / "PulsePay_Product_Analytics_Report.docx"
    )

    document.save(output_file)

    return output_file


def create_pdf(findings):

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        REPORT_DIR / "PulsePay_Product_Analytics_Report.pdf"
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=22,
        leading=28,
        spaceAfter=20,
    )

    story = []

    story.append(
        Paragraph(
            findings["project_title"],
            title_style
        )
    )

    story.append(
        Paragraph(
            "Product Analytics Business Case Study",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 0.3 * inch)
    )

    story.append(
        Paragraph(
            "Executive Summary",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            findings["executive_summary"],
            styles["BodyText"]
        )
    )

    for section in findings["sections"]:

        story.append(
            Spacer(1, 0.2 * inch)
        )

        story.append(
            Paragraph(
                section["title"],
                styles["Heading1"]
            )
        )

        story.append(
            Paragraph(
                section["content"],
                styles["BodyText"]
            )
        )

    story.append(
        Spacer(1, 0.2 * inch)
    )

    story.append(
        Paragraph(
            "Business Recommendations",
            styles["Heading1"]
        )
    )

    for recommendation in findings["recommendations"]:

        story.append(
            Paragraph(
                f"&bull; {recommendation}",
                styles["BodyText"]
            )
        )

    story.append(
        Paragraph(
            "Analytical Limitations",
            styles["Heading1"]
        )
    )

    for limitation in findings.get(
        "limitations",
        []
    ):

        story.append(
            Paragraph(
                f"&bull; {limitation}",
                styles["BodyText"]
            )
        )

    pdf = SimpleDocTemplate(
        str(output_file),
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
    )

    pdf.build(story)

    return output_file


def generate_report():

    findings = load_findings()

    docx_file = create_docx(findings)
    pdf_file = create_pdf(findings)

    print("\n[PASS] Business report generated.")
    print(f"[INFO] DOCX: {docx_file}")
    print(f"[INFO] PDF: {pdf_file}")

    return True

"""
Run:  python generate_report.py
Output: GradeOps_Project_Report.pdf  on the Desktop
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable

DESKTOP = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
OUT_PATH = os.path.join(DESKTOP, "GradeOps_Project_Report.pdf")

# ── Colour palette ────────────────────────────────────────────────────────────
PURPLE      = colors.HexColor("#6d28d9")
PURPLE_DARK = colors.HexColor("#4c1d95")
PURPLE_LIGHT= colors.HexColor("#ede9fe")
DARK        = colors.HexColor("#1e1b2e")
SLATE       = colors.HexColor("#334155")
MUTED       = colors.HexColor("#64748b")
WHITE       = colors.white
RULE_CLR    = colors.HexColor("#ddd6fe")

# ── Styles ────────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=base[parent], **kw)

cover_title   = S("CoverTitle",   fontSize=34, textColor=WHITE,     leading=42, spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
cover_sub     = S("CoverSub",     fontSize=13, textColor=PURPLE_LIGHT, leading=18, spaceAfter=4,  alignment=TA_CENTER, fontName="Helvetica")
cover_meta    = S("CoverMeta",    fontSize=10, textColor=PURPLE_LIGHT, leading=14, spaceAfter=2,  alignment=TA_CENTER, fontName="Helvetica")

h1            = S("H1",           fontSize=15, textColor=PURPLE_DARK, leading=20, spaceBefore=18, spaceAfter=6,  fontName="Helvetica-Bold")
h2            = S("H2",           fontSize=12, textColor=DARK,         leading=16, spaceBefore=12, spaceAfter=4,  fontName="Helvetica-Bold")
body          = S("Body",         fontSize=10, textColor=SLATE,        leading=15, spaceAfter=6,   alignment=TA_JUSTIFY, fontName="Helvetica")
bullet_style  = S("Bullet",       fontSize=10, textColor=SLATE,        leading=14, spaceAfter=3,   leftIndent=14, fontName="Helvetica",
                  bulletIndent=4, bulletFontName="Helvetica", bulletFontSize=10)
code_style    = S("Code",         fontSize=8.5, textColor=DARK,        leading=13, spaceAfter=4,
                  backColor=PURPLE_LIGHT, leftIndent=10, rightIndent=10, borderPadding=(4,6,4,6),
                  fontName="Courier")
caption       = S("Caption",      fontSize=8,  textColor=MUTED,        leading=11, spaceAfter=8,   alignment=TA_CENTER, fontName="Helvetica-Oblique")
footer_style  = S("Footer",       fontSize=8,  textColor=MUTED,        leading=10, alignment=TA_CENTER)

# Usable content width = page width minus left + right margins
USABLE_W = A4[0] - 2 * 2.2 * cm   # ≈ 470.5 pt  (16.6 cm)

# Paragraph styles used inside table cells
tbl_key  = ParagraphStyle("tbl_key",  fontName="Helvetica-Bold", fontSize=9,   leading=13, textColor=PURPLE_DARK)
tbl_val  = ParagraphStyle("tbl_val",  fontName="Helvetica",      fontSize=9,   leading=13, textColor=SLATE)
tbl_head = ParagraphStyle("tbl_head", fontName="Helvetica-Bold", fontSize=8.5, leading=12, textColor=WHITE)
tbl_cell = ParagraphStyle("tbl_cell", fontName="Helvetica",      fontSize=8.5, leading=12, textColor=SLATE)

_STRIPE = colors.HexColor("#f5f3ff")

def rule(): return HRFlowable(width="100%", thickness=1, color=RULE_CLR, spaceAfter=8, spaceBefore=4)
def gap(h=6): return Spacer(1, h)
def bp(): return PageBreak()

def bullet(text): return Paragraph(f"• {text}", bullet_style)

def kv_table(rows, key_width=4.8*cm):
    """Two-column key/value table. All cells are Paragraphs so text wraps."""
    val_width = USABLE_W - key_width
    data = [
        [Paragraph(r[0], tbl_key), Paragraph(r[1], tbl_val)]
        for r in rows
    ]
    t = Table(data, colWidths=[key_width, val_width])
    t.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (0, -1), PURPLE_LIGHT),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, _STRIPE]),
        ("GRID",           (0, 0), (-1, -1), 0.4, RULE_CLR),
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",     (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 6),
        ("LEFTPADDING",    (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 8),
    ]))
    return t

def header_table(rows, headers, col_widths=None):
    """Multi-column table with a coloured header row. All cells are Paragraphs."""
    if col_widths is None:
        col_widths = [USABLE_W / len(headers)] * len(headers)
    hdr = [Paragraph(h, tbl_head) for h in headers]
    body_rows = [[Paragraph(str(c), tbl_cell) for c in row] for row in rows]
    data = [hdr] + body_rows
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0), PURPLE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, _STRIPE]),
        ("GRID",           (0, 0), (-1, -1), 0.4, RULE_CLR),
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",     (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 6),
        ("LEFTPADDING",    (0, 0), (-1, -1), 7),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 7),
    ]))
    return t

# ── Page template with footer ─────────────────────────────────────────────────
class ReportDoc(SimpleDocTemplate):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._page = 0

    def handle_pageBegin(self):
        super().handle_pageBegin()
        self._page += 1

    def afterPage(self):
        c = self.canv
        page = self._page
        if page == 1:
            return
        w, _ = A4
        c.saveState()
        c.setStrokeColor(RULE_CLR)
        c.setLineWidth(0.5)
        c.line(2*cm, 1.6*cm, w - 2*cm, 1.6*cm)
        c.setFont("Helvetica", 7.5)
        c.setFillColor(MUTED)
        c.drawString(2*cm, 1.1*cm, "GradeOps — AI-Powered Exam Grading Platform")
        c.drawRightString(w - 2*cm, 1.1*cm, f"Page {page - 1}")
        c.restoreState()


# ── Build content ─────────────────────────────────────────────────────────────
def build():
    doc = ReportDoc(
        OUT_PATH,
        pagesize=A4,
        leftMargin=2.2*cm, rightMargin=2.2*cm,
        topMargin=2.2*cm,  bottomMargin=2.4*cm,
    )

    story = []

    # ── COVER PAGE ────────────────────────────────────────────────────────────
    # Dark cover block drawn via a single-cell Table
    cover_content = [
        [Paragraph("GradeOps", cover_title)],
        [Paragraph("AI-Powered Exam Grading &amp; Results Management Platform", cover_sub)],
        [gap(14)],
        [Paragraph("Project Technical Report", cover_meta)],
        [Paragraph("May 2026 &nbsp;|&nbsp; Version 1.0", cover_meta)],
        [gap(10)],
        [Paragraph("Krish Patel &nbsp;|&nbsp; Ayush Bansal &nbsp;|&nbsp; Lalit Deshmane", cover_meta)],
    ]
    cover_table = Table([[row[0]] for row in cover_content], colWidths=[USABLE_W])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 20),
        ("RIGHTPADDING",  (0,0), (-1,-1), 20),
        ("ROUNDEDCORNERS", [8]),
    ]))
    story.append(gap(60))
    story.append(cover_table)
    story.append(gap(30))

    badges = [["Python 3.12", "FastAPI", "React 19.2", "Qwen2-VL OCR", "PyMuPDF", "JWT Auth"]]
    bt = Table(badges, colWidths=[2.6*cm]*6)
    bt.setStyle(TableStyle([
        ("BACKGROUND",     (0,0), (-1,-1), PURPLE),
        ("TEXTCOLOR",      (0,0), (-1,-1), WHITE),
        ("FONTNAME",       (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE",       (0,0), (-1,-1), 8),
        ("ALIGN",          (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING",     (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",  (0,0), (-1,-1), 5),
        ("LEFTPADDING",    (0,0), (-1,-1), 4),
        ("RIGHTPADDING",   (0,0), (-1,-1), 4),
        ("ROUNDEDCORNERS", [4]),
    ]))
    story.append(bt)
    story.append(bp())

    # ── PAGE 1 ─────────────────────────────────────────────────────────────────

    # 1. Abstract
    story.append(Paragraph("Abstract", h1))
    story.append(rule())
    story.append(Paragraph(
        "GradeOps is a full-stack, AI-assisted examination grading platform that automates "
        "the evaluation of handwritten and printed answer sheets. The system combines a "
        "Vision-Language Model (Qwen2-VL-2B-OCR) for optical character recognition with a "
        "structured marking scheme evaluator to produce per-question scores, matched and missing "
        "criteria, and natural-language reasoning for each submission. The platform is accessible "
        "through a single-page React dashboard and backed by a FastAPI REST API with JWT "
        "authentication. All data is persisted as flat JSON files, eliminating the need for a "
        "dedicated database.", body))
    story.append(gap(4))

    # 2. Introduction
    story.append(Paragraph("1. Introduction", h1))
    story.append(rule())
    story.append(Paragraph("1.1 Background", h2))
    story.append(Paragraph(
        "Manual evaluation of written examinations remains a significant bottleneck in academic "
        "institutions. A single instructor may be responsible for grading dozens to hundreds of "
        "answer sheets per examination cycle — a process that is time-consuming, subjective, and "
        "prone to inconsistency across evaluators. The rise of large Vision-Language Models capable "
        "of reading handwritten text creates an opportunity to partially automate this workflow "
        "while preserving the nuance of rubric-based grading.", body))

    story.append(Paragraph("1.2 Problem Statement", h2))
    story.append(Paragraph(
        "Traditional grading workflows suffer from three core problems:", body))
    story.append(bullet("<b>Speed:</b> Manual evaluation of a 30-question paper for 60 students can exceed 40 person-hours."))
    story.append(bullet("<b>Consistency:</b> Subjective judgement varies between evaluators and even within a single evaluator across a session."))
    story.append(bullet("<b>Traceability:</b> Paper-based records lack structured storage, making historical analysis and appeals difficult."))
    story.append(gap(4))

    story.append(Paragraph("1.3 Objectives", h2))
    story.append(bullet("Automate OCR extraction of handwritten and printed answer sheets using a Vision-Language Model."))
    story.append(bullet("Evaluate extracted text against instructor-defined marking schemes with configurable strictness."))
    story.append(bullet("Provide per-question scoring with matched/missing criteria and reasoning."))
    story.append(bullet("Deliver a secure, instructor-facing REST API and a responsive single-page dashboard."))
    story.append(bullet("Accept answer sheets and marking schemes in both image and PDF formats."))
    story.append(gap(6))

    # 3. System Architecture
    story.append(Paragraph("2. System Architecture", h1))
    story.append(rule())
    story.append(Paragraph(
        "GradeOps is structured as a decoupled two-tier system: a React single-page application "
        "communicating with a FastAPI backend via authenticated REST calls. The backend itself is "
        "further decomposed into an API orchestration layer and an AI inference pipeline.", body))

    story.append(Paragraph("2.1 Component Overview", h2))
    story.append(kv_table([
        ["Instructor Portal",     "React 19.2 SPA — single-page dashboard with a persistent sticky sidebar and collapsible accordion sections for Exams, Students, and Results."],
        ["API Orchestrator",      "FastAPI backend exposing six route modules (Auth, Exams, Students, OCR, Evaluate, Submissions) behind JWT Bearer authentication."],
        ["File Normalisation",    "PyMuPDF (fitz) renders multi-page PDFs to stacked PIL images at 200 DPI; JPEG/PNG inputs are opened directly via Pillow."],
        ["Vision OCR Engine",     "Qwen2-VL-2B-OCR (HuggingFace Transformers + PyTorch) extracts plain-text transcripts from normalised images, up to 2 048 tokens per sheet."],
        ["Evaluation Engine",     "Compares extracted transcript against each question's expected_points and keywords arrays, applying a strictness modifier to compute partial or full marks."],
        ["JSON File Store",       "All records (users, exams, students, schemes, submissions, evaluations) are persisted as structured flat JSON files under data/ — no external DB required."],
    ]))
    story.append(gap(6))

    story.append(Paragraph("2.2 Request Lifecycle — Answer Sheet Grading", h2))
    lifecycle = [
        ["Step", "Actor", "Action"],
        ["1", "Frontend", "Instructor submits exam_id, student_id, and answer sheet file via multipart POST /evaluate/grade"],
        ["2", "Auth Guard", "JWT token extracted from Bearer header; instructor identity resolved"],
        ["3", "Route Handler", "File saved to uploads/; marking scheme retrieved from JSON store"],
        ["4", "Image Loader", "If PDF: PyMuPDF renders pages → stacked PIL image. If image: PIL opens directly"],
        ["5", "OCR Service", "Qwen2-VL-2B-OCR tokenises image and generates text transcript"],
        ["6", "Evaluator", "Transcript scored per-question against expected_points / keywords with strictness weighting"],
        ["7", "Store", "Submission and evaluation records written to data/submissions/ and data/evaluations/"],
        ["8", "Response", "JSON payload returned: scores, percentage, question_wise breakdown, overall_reasoning"],
    ]
    # Step | Actor | Action  —  narrow / medium / wide
    story.append(header_table(
        lifecycle[1:], lifecycle[0],
        col_widths=[1.4*cm, 3.4*cm, USABLE_W - 4.8*cm],
    ))
    story.append(bp())

    # ── PAGE 2 ─────────────────────────────────────────────────────────────────

    # 4. Technology Stack
    story.append(Paragraph("3. Technology Stack", h1))
    story.append(rule())

    story.append(Paragraph("3.1 Backend", h2))
    story.append(kv_table([
        ["Python 3.12",       "Primary runtime for all backend services and data processing."],
        ["FastAPI",           "Async REST framework with automatic OpenAPI/Swagger documentation at /docs."],
        ["Uvicorn",           "ASGI server for serving the FastAPI application."],
        ["Pydantic v2",       "Request/response schema validation and environment configuration via pydantic-settings."],
        ["python-jose",       "JWT token encoding, decoding, and expiry verification."],
        ["Passlib + bcrypt",  "Password hashing and verification for instructor accounts."],
        ["PyMuPDF (fitz)",    "PDF rendering and text extraction — converts PDF pages to PIL images for OCR."],
        ["Pillow",            "Image loading, format conversion, and multi-page stitching."],
    ]))
    story.append(gap(8))

    story.append(Paragraph("3.2 AI / ML", h2))
    story.append(kv_table([
        ["Qwen2-VL-2B-OCR",  "Vision-Language Model by JackChew (HuggingFace) — fine-tuned for document OCR on the Qwen2-VL architecture."],
        ["Transformers",      "HuggingFace library for model loading, tokenisation, and autoregressive inference."],
        ["PyTorch",           "Deep learning runtime; CUDA GPU acceleration supported (CPU fallback available)."],
        ["Accelerate",        "HuggingFace utility for automatic device placement (CPU / single GPU / multi-GPU)."],
    ]))
    story.append(gap(8))

    story.append(Paragraph("3.3 Frontend", h2))
    story.append(kv_table([
        ["React 19.2",        "Component-based SPA framework with hooks for state and side-effects."],
        ["React Router v7",   "Client-side routing with ProtectedRoute guards; legacy /exams /students /results redirect to /dashboard."],
        ["Vite 8.0",          "Next-generation frontend build tool with HMR (Hot Module Replacement) for fast development."],
        ["Axios",             "Promise-based HTTP client; all API calls attach a Bearer token from AuthContext."],
        ["IntersectionObserver", "Used in Sidebar.jsx to detect which section is in the viewport for scroll-spy active highlighting."],
    ]))
    story.append(gap(6))

    # 5. Key Features
    story.append(Paragraph("4. Key Features &amp; Implementation", h1))
    story.append(rule())

    story.append(Paragraph("4.1 Marking Scheme Upload", h2))
    story.append(Paragraph(
        "Instructors upload a marking scheme linked to a specific exam. The scheme follows a "
        "structured JSON format defining, for each question: <b>question_no</b>, <b>max_marks</b>, "
        "<b>expected_points</b> (list of expected answer criteria), <b>keywords</b> (key terms that "
        "signal understanding), and a <b>strictness</b> level. Both raw JSON files and "
        "text-extractable PDFs are accepted. For PDFs, PyMuPDF's <i>page.get_text()</i> extracts "
        "embedded text before JSON parsing; image-based (scanned) PDFs are rejected with a "
        "descriptive error.", body))
    story.append(Paragraph("Scheme JSON structure:", body))
    story.append(Paragraph(
        '{ "exam_name": "...", "total_marks": 30, "questions": [ { "question_no": 1, '
        '"max_marks": 10, "expected_points": ["..."], "keywords": ["..."], "strictness": "medium" } ] }',
        code_style))
    story.append(gap(4))

    story.append(Paragraph("4.2 AI Answer Sheet Grading", h2))
    story.append(Paragraph(
        "Answer sheets are submitted as JPEG, PNG, or PDF uploads. The grading pipeline operates "
        "in four stages: (1) file normalisation via PyMuPDF/Pillow, (2) OCR transcript generation "
        "by Qwen2-VL-2B-OCR, (3) per-question evaluation against the marking scheme, and "
        "(4) aggregation into a final score, percentage, and structured question-wise breakdown. "
        "Each question result includes <b>awarded_marks</b>, <b>matched_points</b>, "
        "<b>missing_points</b>, and a <b>reasoning</b> string explaining the score.", body))

    story.append(Paragraph("4.3 Single-Page Instructor Dashboard", h2))
    story.append(Paragraph(
        "The frontend consolidates the Exams, Students, and Results workflows into a single "
        "scrollable page with collapsible accordion sections. A persistent sticky sidebar uses "
        "the browser's <i>IntersectionObserver</i> API to automatically highlight the active section "
        "as the instructor scrolls. Clicking a sidebar item smoothly scrolls to the corresponding "
        "section anchor. The student list includes a live search bar filtering by name or student "
        "ID without a server round-trip.", body))

    story.append(Paragraph("4.4 Authentication &amp; Security", h2))
    story.append(bullet("<b>Password hashing:</b> bcrypt via Passlib — plaintext passwords are never stored."))
    story.append(bullet("<b>JWT tokens:</b> HS256-signed tokens with configurable expiry (default 60 min) issued on successful login."))
    story.append(bullet("<b>Auth guard:</b> A FastAPI Depends() decorator on every protected route extracts and verifies the Bearer token, resolving the instructor identity."))
    story.append(bullet("<b>CORS:</b> Configured in main.py — origins should be restricted to the frontend URL in production."))
    story.append(gap(6))

    # 6. API Reference
    story.append(Paragraph("5. API Reference", h1))
    story.append(rule())
    api_rows = [
        ["POST", "/auth/register",                  "Register a new instructor account"],
        ["POST", "/auth/login",                     "Authenticate and receive a JWT token"],
        ["POST", "/exams/create",                   "Create a new exam record"],
        ["GET",  "/exams/",                         "List all exams for the authenticated instructor"],
        ["POST", "/students/create",                "Register a new student"],
        ["GET",  "/students/",                      "List all students"],
        ["POST", "/evaluate/upload-scheme",         "Upload a marking scheme (JSON or text PDF)"],
        ["POST", "/evaluate/grade",                 "Grade an answer sheet (image or PDF) via OCR + evaluator"],
        ["GET",  "/submissions/exam/{exam_id}",     "Retrieve all evaluation results for a given exam"],
        ["GET",  "/submissions/student/{student_id}", "Retrieve all evaluation results for a given student"],
    ]
    # Method | Endpoint | Description  —  narrow / medium / wide
    story.append(header_table(
        api_rows, ["Method", "Endpoint", "Description"],
        col_widths=[1.8*cm, 7.2*cm, USABLE_W - 9.0*cm],
    ))
    story.append(Paragraph(
        "All endpoints except /auth/* require Authorization: Bearer &lt;token&gt; in the request header.",
        caption))
    story.append(gap(4))

    # 7. Environment Configuration
    story.append(Paragraph("6. Environment Configuration", h1))
    story.append(rule())
    story.append(Paragraph(
        "Runtime behaviour is controlled via a .env file in the backend/ directory:", body))
    story.append(kv_table([
        ["MODEL_NAME",    "HuggingFace model ID for OCR inference (default: JackChew/Qwen2-VL-2B-OCR)"],
        ["MAX_NEW_TOKENS","Maximum token output per OCR pass (default: 2048)"],
        ["UPLOAD_DIR",    "Directory where answer sheet files are saved (default: uploads/)"],
        ["DATA_DIR",      "Root directory for all JSON data stores (default: data/)"],
        ["JWT_SECRET_KEY","Secret key for HS256 token signing — must be changed in production"],
        ["ACCESS_TOKEN_EXPIRE_MINUTES", "JWT token lifetime in minutes (default: 60)"],
    ]))
    story.append(gap(6))

    # 8. Conclusion
    story.append(Paragraph("7. Conclusion &amp; Future Work", h1))
    story.append(rule())
    story.append(Paragraph(
        "GradeOps demonstrates that a Vision-Language Model can meaningfully automate structured "
        "exam grading when paired with a well-defined marking scheme. The current implementation "
        "covers the complete instructor workflow — from exam creation and student registration to "
        "AI-graded submissions and results lookup — within a lightweight, dependency-minimal stack.", body))
    story.append(Paragraph("Identified areas for future development include:", body))
    story.append(bullet("<b>Database backend:</b> Migrate from flat JSON to PostgreSQL or SQLite for concurrent access and query performance."))
    story.append(bullet("<b>Bulk upload:</b> Accept a ZIP of answer sheets and process them asynchronously with a task queue (Celery / ARQ)."))
    story.append(bullet("<b>Larger OCR models:</b> Evaluate Qwen2-VL-7B or GPT-4o Vision for improved handwriting recognition accuracy."))
    story.append(bullet("<b>Scanned PDF scheme support:</b> Add OCR-to-JSON extraction for image-based marking scheme PDFs."))
    story.append(bullet("<b>Appeals workflow:</b> Allow instructors to manually override individual question scores with a reason."))
    story.append(bullet("<b>Analytics:</b> Add class-level statistics — score distributions, question difficulty analysis, cohort comparisons."))

    doc.build(story)
    print(f"Report saved to: {OUT_PATH}")


if __name__ == "__main__":
    build()

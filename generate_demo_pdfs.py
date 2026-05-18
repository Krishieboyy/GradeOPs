"""
Run from the backend venv:
  python generate_demo_pdfs.py

Outputs two PDFs on the Desktop:
  demo_scheme.pdf        — marking scheme (JSON text, upload via Upload Scheme)
  demo_answer_sheet.pdf  — partial student answer sheet (upload via Grade Answer Sheet)
"""

import fitz  # pymupdf
import json
import os

DESKTOP = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")


# ── helpers ──────────────────────────────────────────────────────────────────

def write_pdf(text: str, path: str, fontname: str = "Courier", fontsize: float = 9.0):
    """Write multi-page A4 PDF from plain text, paginating automatically."""
    doc = fitz.open()
    W, H = 595, 842          # A4 points
    margin_x, margin_top = 50, 55
    line_h = fontsize * 1.45
    usable_h = H - margin_top - 40
    lines_per_page = int(usable_h / line_h)

    lines = text.splitlines()
    for start in range(0, max(len(lines), 1), lines_per_page):
        page = doc.new_page(width=W, height=H)
        chunk = "\n".join(lines[start : start + lines_per_page])
        page.insert_text(
            (margin_x, margin_top),
            chunk,
            fontsize=fontsize,
            fontname=fontname,
            color=(0, 0, 0),
        )
    doc.save(path)
    doc.close()
    print(f"  created: {path}")


# ── 1. Marking Scheme PDF ─────────────────────────────────────────────────────

scheme = {
    "exam_name": "Introduction to Computer Science",
    "total_marks": 30,
    "questions": [
        {
            "question_no": 1,
            "max_marks": 10,
            "expected_points": [
                "An operating system manages hardware and software resources",
                "It provides a user interface and services for application programs",
                "Examples include Windows, Linux, and macOS",
            ],
            "keywords": ["operating system", "hardware", "software", "resources", "kernel", "interface"],
            "strictness": "medium",
        },
        {
            "question_no": 2,
            "max_marks": 10,
            "expected_points": [
                "RAM stands for Random Access Memory",
                "It is volatile — data is lost when power is removed",
                "RAM stores currently running programs and active data",
                "More RAM allows more programs to run simultaneously",
            ],
            "keywords": ["RAM", "volatile", "memory", "temporary", "random access", "primary storage"],
            "strictness": "medium",
        },
        {
            "question_no": 3,
            "max_marks": 10,
            "expected_points": [
                "The CPU (Central Processing Unit) fetches, decodes, and executes instructions",
                "It contains the ALU (Arithmetic Logic Unit) for calculations",
                "The Control Unit coordinates all CPU operations",
                "Clock speed in GHz measures how many cycles per second the CPU performs",
            ],
            "keywords": ["CPU", "processor", "ALU", "control unit", "instructions", "clock speed", "GHz", "fetch", "decode"],
            "strictness": "medium",
        },
    ],
}

scheme_text = json.dumps(scheme, indent=2)
scheme_path = os.path.join(DESKTOP, "demo_scheme.pdf")
write_pdf(scheme_text, scheme_path, fontname="Courier", fontsize=8.5)


# ── 2. Partial Answer Sheet PDF ───────────────────────────────────────────────

answer_sheet = """\
ANSWER SHEET
============================================================
Student Name : Alex Johnson
Student ID   : STU001
Exam         : Introduction to Computer Science
Date         : 18 May 2026
============================================================

Question 1  (10 marks)
What is an Operating System? Give examples.

An operating system is system software that manages the hardware
and software resources of a computer. It provides an interface
between the user and the computer hardware. Common examples of
operating systems are Windows, Linux, and macOS.

------------------------------------------------------------

Question 2  (10 marks)
Define RAM. Explain its role and key characteristics.

RAM is Random Access Memory. It is used by the computer to
store data and programs that are currently in use. RAM is
temporary storage — the data is lost when the computer is
switched off.

------------------------------------------------------------

Question 3  (10 marks)
Describe the role of the CPU in a computer system.

[No answer provided]

============================================================
"""

sheet_path = os.path.join(DESKTOP, "demo_answer_sheet.pdf")
write_pdf(answer_sheet, sheet_path, fontname="Times-Roman", fontsize=11.0)

print("Done.")

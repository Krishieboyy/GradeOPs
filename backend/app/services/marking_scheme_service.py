import json
import fitz  # pymupdf
from app.schemas.evaluation_schema import MarkingScheme
from app.storage.scheme_store import create_scheme
from app.storage.exam_store import get_exam_by_exam_id, attach_scheme_to_exam


def _parse_scheme_bytes(file_bytes: bytes, filename: str) -> dict:
    """Return a dict from a JSON file or a text-based PDF containing JSON."""
    if filename.lower().endswith(".pdf"):
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = "".join(page.get_text() for page in doc).strip()
        doc.close()
        if not text:
            raise ValueError(
                "No selectable text found in the PDF. "
                "Please use a text-based PDF (not a scan) or upload a JSON file."
            )
        return json.loads(text)
    return json.loads(file_bytes.decode("utf-8"))


def upload_marking_scheme(exam_id: str, uploaded_by: str, file_bytes: bytes, filename: str = ""):
    exam = get_exam_by_exam_id(exam_id)
    if not exam:
        return None, "Exam not found"

    try:
        data = _parse_scheme_bytes(file_bytes, filename)
        scheme = MarkingScheme(**data)
    except (json.JSONDecodeError, ValueError) as e:
        return None, f"Invalid scheme file: {e}"
    except Exception as e:
        return None, f"Failed to parse scheme: {e}"

    created = create_scheme(exam_id, uploaded_by, scheme.model_dump())
    attach_scheme_to_exam(exam_id, created["scheme_id"])

    return {
        "scheme_id": created["scheme_id"],
        "exam_id": exam_id,
        "exam_name": created["exam_name"],
        "total_marks": created["total_marks"],
        "question_count": len(created["questions"])
    }, None

import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.config import UPLOAD_DIR
from app.utils.image_loader import load_image
from app.services.ocr_service import extract_text_from_image
from app.services.marking_scheme_service import upload_marking_scheme
from app.services.evaluation_service import evaluate_answer_text
from app.storage.scheme_store import load_scheme
from app.schemas.evaluation_schema import SchemeUploadResponse, EvaluationResponse

router = APIRouter()

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-scheme", response_model=SchemeUploadResponse)
async def upload_scheme(file: UploadFile = File(...)):
    try:
        content = await file.read()
        result = upload_marking_scheme(content)
        return SchemeUploadResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/grade", response_model=EvaluationResponse)
async def grade_answer_sheet(
    answer_sheet: UploadFile = File(...),
    scheme_id: str = Form(...)
):
    try:
        scheme = load_scheme(scheme_id)
        if not scheme:
            raise HTTPException(status_code=404, detail="Marking scheme not found")

        file_path = os.path.join(UPLOAD_DIR, answer_sheet.filename)
        with open(file_path, "wb") as f:
            f.write(await answer_sheet.read())

        image = load_image(file_path)
        extracted_text = extract_text_from_image(image)

        result = evaluate_answer_text(extracted_text, scheme)
        result.scheme_id = scheme_id
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
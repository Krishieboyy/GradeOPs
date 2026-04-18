from pydantic import BaseModel
from typing import List, Optional

class SchemeQuestion(BaseModel):
    question_no: int
    max_marks: float
    expected_points: List[str]
    keywords: List[str] = []
    strictness: str = "medium"

class MarkingScheme(BaseModel):
    exam_name: str
    total_marks: float
    questions: List[SchemeQuestion]

class SchemeUploadResponse(BaseModel):
    scheme_id: str
    exam_id: str
    exam_name: str
    total_marks: float
    question_count: int

class QuestionEvaluation(BaseModel):
    question_no: int
    awarded_marks: float
    max_marks: float
    matched_points: List[str]
    missing_points: List[str]
    reasoning: str

class EvaluationResponse(BaseModel):
    evaluation_id: str
    submission_id: str
    scheme_id: str
    exam_id: str
    student_id: str
    extracted_text: str
    total_score: float
    max_score: float
    percentage: float
    question_wise: List[QuestionEvaluation]
    overall_reasoning: str
    created_at: str
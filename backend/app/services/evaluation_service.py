import re
from app.schemas.evaluation_schema import QuestionEvaluation

def normalize_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{2,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

def score_question(answer_text: str, q: dict):
    answer_lower = answer_text.lower()

    matched_points = []
    missing_points = []

    for point in q["expected_points"]:
        point_words = point.lower().split()
        if not point_words:
            continue

        hit_count = sum(1 for w in point_words if w in answer_lower)
        ratio = hit_count / len(point_words)

        if ratio >= 0.5:
            matched_points.append(point)
        else:
            missing_points.append(point)

    score = 0.0
    if q["expected_points"]:
        score = (len(matched_points) / len(q["expected_points"])) * q["max_marks"]

    score = round(min(score, q["max_marks"]), 2)

    reasoning = (
        "Good coverage of expected points."
        if score >= 0.75 * q["max_marks"]
        else "Partial coverage of expected points."
        if score >= 0.4 * q["max_marks"]
        else "Limited match with expected points."
    )

    return QuestionEvaluation(
        question_no=q["question_no"],
        awarded_marks=score,
        max_marks=q["max_marks"],
        matched_points=matched_points,
        missing_points=missing_points,
        reasoning=reasoning
    )

def evaluate_answer_text(extracted_text: str, scheme: dict):
    clean_text = normalize_text(extracted_text)

    results = []
    total_score = 0.0

    for q in scheme["questions"]:
        res = score_question(clean_text, q)
        results.append(res)
        total_score += res.awarded_marks

    max_score = scheme["total_marks"]
    percentage = round((total_score / max_score) * 100, 2) if max_score else 0.0

    overall_reasoning = (
        "Strong overall performance."
        if percentage >= 75
        else "Moderate performance with some missing points."
        if percentage >= 40
        else "Low alignment with marking scheme."
    )

    return {
        "extracted_text": clean_text,
        "total_score": round(total_score, 2),
        "max_score": max_score,
        "percentage": percentage,
        "question_wise": [r.model_dump() for r in results],
        "overall_reasoning": overall_reasoning
    }
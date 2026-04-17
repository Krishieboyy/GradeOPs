import re
from app.schemas.evaluation_schema import QuestionEvaluation, EvaluationResponse

def normalize_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{2,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

def score_question(answer_text: str, q: dict) -> QuestionEvaluation:
    answer_lower = answer_text.lower()

    matched_points = []
    missing_points = []

    keyword_hits = 0
    total_keywords = max(len(q.get("keywords", [])), 1)

    for kw in q.get("keywords", []):
        if kw.lower() in answer_lower:
            keyword_hits += 1

    for point in q["expected_points"]:
        point_words = point.lower().split()
        hit_count = sum(1 for w in point_words if w in answer_lower)

        if len(point_words) == 0:
            continue

        ratio = hit_count / len(point_words)

        if ratio >= 0.5:
            matched_points.append(point)
        else:
            missing_points.append(point)

    point_score = 0.0
    if q["expected_points"]:
        point_score = (len(matched_points) / len(q["expected_points"])) * q["max_marks"]

    keyword_bonus = 0.0
    if q.get("keywords"):
        keyword_bonus = (keyword_hits / total_keywords) * 0.2 * q["max_marks"]

    awarded = min(q["max_marks"], round(point_score * 0.8 + keyword_bonus, 2))

    reasoning = (
        "Good coverage of expected points."
        if awarded >= 0.75 * q["max_marks"]
        else "Partial coverage of expected points."
        if awarded >= 0.4 * q["max_marks"]
        else "Limited match with expected points."
    )

    return QuestionEvaluation(
        question_no=q["question_no"],
        awarded_marks=awarded,
        max_marks=q["max_marks"],
        matched_points=matched_points,
        missing_points=missing_points,
        reasoning=reasoning
    )

def evaluate_answer_text(extracted_text: str, scheme: dict) -> EvaluationResponse:
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

    return EvaluationResponse(
        scheme_id="",
        extracted_text=clean_text,
        total_score=round(total_score, 2),
        max_score=max_score,
        percentage=percentage,
        question_wise=results,
        overall_reasoning=overall_reasoning
    )
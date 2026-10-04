from courses import get_grade_point


def process_subject_marks(course_dict: dict, cca1: float, cca2: float, assignment: float, endsem: float,
                          target_grade_pts: int = 8):
    weights = course_dict["weightage"]

    # Check which assessments are missing (entered as None or < 0)
    given_score = 0.0
    weight_completed = 0.0

    if cca1 is not None:
        given_score += cca1 * (weights["cca1"] / 100.0)
        weight_completed += weights["cca1"]
    if cca2 is not None:
        given_score += cca2 * (weights["cca2"] / 100.0)
        weight_completed += weights["cca2"]
    if assignment is not None:
        given_score += assignment * (weights["assignment"] / 100.0)
        weight_completed += weights["assignment"]
    if endsem is not None:
        given_score += endsem * (weights["endsem"] / 100.0)
        weight_completed += weights["endsem"]

    weight_remaining = 100.0 - weight_completed

    # Target cutoffs: S=90, A=80, B=70
    target_pct = 80.0 if target_grade_pts == 9 else (90.0 if target_grade_pts == 10 else 70.0)

    suggestion_msg = ""
    needed_score = 0.0

    if weight_remaining > 0:
        needed_score = (target_pct - given_score) / (weight_remaining / 100.0)
        needed_score = round(max(0.0, needed_score), 1)
        suggestion_msg = f"Obtain at least {needed_score}% in remaining evaluations for Grade '{target_grade_pts} pts'."

    # Calculate current percentage on completed weightage
    total_pct = given_score + (needed_score * (weight_remaining / 100.0) if weight_remaining > 0 else 0)
    grade_point, letter_grade = get_grade_point(total_pct)
    credits = course_dict["credits"]

    return {
        "course_code": course_dict["code"],
        "course_name": course_dict["name"],
        "credits": credits,
        "total_pct": round(total_pct, 1),
        "grade_point": grade_point,
        "letter_grade": letter_grade,
        "credit_points": grade_point * credits,
        "suggestion": suggestion_msg,
        "is_predicted": weight_remaining > 0
    }
import numpy as np


def clean_numpy(obj):
    """
    Convert NumPy types to normal Python types
    so MongoDB can save them.
    """

    if isinstance(obj, dict):
        return {k: clean_numpy(v) for k, v in obj.items()}

    elif isinstance(obj, list):
        return [clean_numpy(v) for v in obj]

    elif isinstance(obj, np.bool_):
        return bool(obj)

    elif isinstance(obj, np.integer):
        return int(obj)

    elif isinstance(obj, np.floating):
        return float(obj)

    return obj


def compute_final_score(
    face_data,
    attention_data,
    eye_contact_data,
    audio_data,
    transcript_data
):

    face_visibility = face_data.get("face_visibility", 0)
    multiple_face_ratio = face_data.get("multiple_face_ratio", 0)

    attention_score = (
        attention_data or {}
    ).get(
        "attention_score",
        0
    )

    eye_contact_score = (
        eye_contact_data or {}
    ).get(
        "eye_contact_score",
        0
    )

    speech_ratio = (
        audio_data or {}
    ).get(
        "speech_ratio",
        0
    )

    word_count = (
        transcript_data or {}
    ).get(
        "word_count",
        0
    )

    cheating_penalty = multiple_face_ratio * 0.5

    transcript_score = min(word_count, 100)

    # TOTAL = 100%
    final_score = (
        (face_visibility * 0.20)
        + (attention_score * 0.25)
        + (eye_contact_score * 0.20)
        + (speech_ratio * 0.20)
        + (transcript_score * 0.15)
    ) - cheating_penalty

    final_score = max(
        0,
        min(100, final_score)
    )

    # HARD FAIL RULES
    mandatory_fail = False

    if attention_score < 20:
        mandatory_fail = True

    if speech_ratio < 20:
        mandatory_fail = True

    if word_count < 10:
        mandatory_fail = True

    if mandatory_fail:
        status = "Disqualified"
        grade = "Poor Performance"

    elif final_score >= 80:
        status = "Qualified"
        grade = "Gold"

    elif final_score >= 65:
        status = "Qualified"
        grade = "Silver"

    elif final_score >= 50:
        status = "Qualified"
        grade = "Bronze"

    else:
        status = "Disqualified"
        grade = "Poor Performance"

    reasons = []

    if face_visibility < 50:
        reasons.append(
            "Low face visibility detected"
        )

    if attention_score < 50:
        reasons.append(
            "Low attention detected"
        )

    if eye_contact_score < 50:
        reasons.append(
            "Poor eye contact detected"
        )

    if multiple_face_ratio > 5:
        reasons.append(
            "Multiple faces detected (possible malpractice)"
        )

    if speech_ratio < 40:
        reasons.append(
            "Very low speaking activity detected"
        )

    if word_count < 20:
        reasons.append(
            "Insufficient explanation provided"
        )

    if len(reasons) == 0:
        reasons.append(
            "Good engagement throughout video"
        )

    result = {
        "face_visibility": round(face_visibility, 2),
        "attention_score": round(attention_score, 2),
        "eye_contact_score": round(eye_contact_score, 2),
        "speech_ratio": round(speech_ratio, 2),
        "word_count": int(word_count),
        "multiple_face_ratio": round(multiple_face_ratio, 2),
        "final_score": round(final_score, 2),
        "status": status,
        "grade": grade,
        "reasons": reasons
    }

    return clean_numpy(result)
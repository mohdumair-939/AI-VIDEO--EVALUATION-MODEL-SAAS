def analyze_engagement(
    attention_data,
    eye_contact_data
):

    attention_score = (
        attention_data.get(
            "attention_score",
            0
        )
    )

    eye_contact_score = (
        eye_contact_data.get(
            "eye_contact_score",
            0
        )
    )

    engagement_score = (
        attention_score * 0.6
        +
        eye_contact_score * 0.4
    )

    return {
        "engagement_score": round(
            engagement_score,
            2
        )
    }
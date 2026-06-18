def generate_feedback(
    relevance,
    coverage,
    communication
):

    feedback = []

    if relevance < 60:

        feedback.append(
            "Explanation is not strongly related to assigned topic."
        )

    if coverage < 60:

        feedback.append(
            "Several key concepts are missing."
        )

    if communication < 40:

        feedback.append(
            "Explanation needs more detail."
        )

    if len(feedback) == 0:

        feedback.append(
            "Good understanding demonstrated."
        )

    return feedback
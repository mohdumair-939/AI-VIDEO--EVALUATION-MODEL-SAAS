def generate_recommendation(
    final_score
):

    if final_score >= 75:

        return {
            "decision": "Completed",
            "action":
            "Proceed to next module"
        }

    elif final_score >= 50:

        return {
            "decision":
            "Needs Improvement",

            "action":
            "Re-submit assignment"
        }

    else:

        return {
            "decision":
            "Rejected",

            "action":
            "Re-learn topic and re-submit"
        }
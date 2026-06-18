from difflib import SequenceMatcher


def analyze_knowledge(transcript_text):

    if not transcript_text:
        return {
            "knowledge_score": 0,
            "depth_score": 0
        }

    transcript = transcript_text.lower()

    depth_words = [
        "because",
        "therefore",
        "used for",
        "helps",
        "advantage",
        "example",
        "for instance",
        "explains",
        "process",
        "logic"
    ]

    depth_count = 0

    for word in depth_words:
        if word in transcript:
            depth_count += 1

    depth_score = min(
        100,
        depth_count * 10
    )

    sentence_count = len(
        transcript.split(".")
    )

    explanation_score = min(
        100,
        sentence_count * 5
    )

    knowledge_score = (
        depth_score * 0.6
        +
        explanation_score * 0.4
    )

    return {
        "knowledge_score": round(
            knowledge_score,
            2
        ),
        "depth_score": round(
            depth_score,
            2
        )
    }
def analyze_confidence(
    audio_data,
    transcript_data
):

    speech_ratio = (
        audio_data.get(
            "speech_ratio",
            0
        )
    )

    word_count = (
        transcript_data.get(
            "word_count",
            0
        )
    )

    confidence = (
        speech_ratio * 0.5
        +
        min(word_count, 100) * 0.5
    )

    return {
        "confidence_score": round(
            confidence,
            2
        )
    }
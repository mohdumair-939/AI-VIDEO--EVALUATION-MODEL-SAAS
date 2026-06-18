def analyze_communication(
    transcript
):

    words = transcript.split()

    word_count = len(words)

    unique_words = len(
        set(words)
    )

    diversity = 0

    if word_count > 0:

        diversity = (
            unique_words
            /
            word_count
        ) * 100

    return {

        "word_count":
        word_count,

        "unique_words":
        unique_words,

        "vocabulary_score":
        round(
            diversity,
            2
        )
    }
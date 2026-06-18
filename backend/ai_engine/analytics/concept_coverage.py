def analyze_concept_coverage(
    transcript,
    expected_concepts
):

    transcript = transcript.lower()

    found = []

    for concept in expected_concepts:

        if concept.lower() in transcript:
            found.append(concept)

    coverage_score = (
        len(found)
        /
        max(
            len(expected_concepts),
            1
        )
    ) * 100

    return {
        "expected_concepts":
        expected_concepts,

        "covered_concepts":
        found,

        "coverage_score":
        round(
            coverage_score,
            2
        )
    }
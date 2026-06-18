from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def evaluate_explanation(
    transcript,
    topic
):

    prompt = f"""
Topic:
{topic}

Student Explanation:
{transcript}

Evaluate:

1. Understanding (0-100)
2. Accuracy (0-100)
3. Completeness (0-100)
4. Practical Knowledge (0-100)

Return JSON only.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text
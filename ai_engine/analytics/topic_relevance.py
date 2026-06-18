from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def analyze_topic_relevance(
    assigned_topic,
    transcript
):

    if not transcript:
        return {
            "relevance_score": 0
        }

    topic_embedding = model.encode(
        [assigned_topic]
    )

    transcript_embedding = model.encode(
        [transcript]
    )

    score = cosine_similarity(
        topic_embedding,
        transcript_embedding
    )[0][0]

    return {
        "relevance_score":
        round(score * 100, 2)
    }
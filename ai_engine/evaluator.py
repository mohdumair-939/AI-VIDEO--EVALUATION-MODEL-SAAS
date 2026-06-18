from ai_engine.utils.normalizer import clean_dict
from ai_engine.scoring import compute_final_score

from ai_engine.face_detection import analyze_face
from ai_engine.attention import analyze_attention
from ai_engine.audio_analysis import analyze_audio
from ai_engine.transcription import transcribe_video
from ai_engine.video_quality import check_video_quality

from ai_engine.analytics.eye_contact import analyze_eye_contact
from ai_engine.analytics.topic_relevance import analyze_topic_relevance
from ai_engine.analytics.concept_coverage import analyze_concept_coverage
from ai_engine.analytics.communication import analyze_communication
from ai_engine.analytics.ai_feedback import generate_feedback

from ai_engine.analytics.knowledge_score import analyze_knowledge
from ai_engine.analytics.confidence_score import analyze_confidence
from ai_engine.analytics.engagement import analyze_engagement
from ai_engine.analytics.recommendation import generate_recommendation


def evaluate_video(video_path, task=None):

    try:

        # -------------------------
        # QUALITY GATE
        # -------------------------
        quality = check_video_quality(video_path)

        if not quality.get("is_valid"):
            return clean_dict({
                "success": False,
                "stage": "quality_failed",
                "quality": quality
            })

        # -------------------------
        # CORE ANALYSIS
        # -------------------------
        face = analyze_face(video_path)
        attention = analyze_attention(video_path)
        eye_contact = analyze_eye_contact(video_path)
        audio = analyze_audio(video_path)
        transcript = transcribe_video(video_path)

        transcript_text = transcript.get("transcript", "")

        # -------------------------
        # TASK LAYER (REAL SaaS LOGIC)
        # -------------------------
        if task:
            topic = task.get("topic", "")
            expected_concepts = task.get("expected_concepts", [])
        else:
            topic = "General"
            expected_concepts = []

        # -------------------------
        # DOMAIN ANALYTICS
        # -------------------------
        topic_relevance = analyze_topic_relevance(topic, transcript_text)

        concept_coverage = analyze_concept_coverage(
            transcript_text,
            expected_concepts
        )

        communication = analyze_communication(transcript_text)

        feedback = generate_feedback(
            topic_relevance.get("relevance_score", 0),
            concept_coverage.get("coverage_score", 0),
            communication.get("vocabulary_score", 0)
        )

        # -------------------------
        # AI SaaS LAYERS
        # -------------------------
        knowledge = analyze_knowledge(transcript_text)
        confidence = analyze_confidence(audio, transcript)
        engagement = analyze_engagement(attention, eye_contact)

        # -------------------------
        # FINAL SCORING ENGINE
        # -------------------------
        final = compute_final_score(
            face,
            attention,
            eye_contact,
            audio,
            transcript
        )

        # -------------------------
        # RECOMMENDATION ENGINE
        # -------------------------
        recommendation = generate_recommendation(
            final.get("final_score", 0)
        )

        # -------------------------
        # OUTPUT (SAAS FORMAT)
        # -------------------------
        return clean_dict({
            "success": True,

            "quality": quality,
            "face": face,
            "attention": attention,
            "eye_contact": eye_contact,
            "audio": audio,
            "transcript": transcript,

            "task": task,

            "topic_relevance": topic_relevance,
            "concept_coverage": concept_coverage,
            "communication": communication,

            "knowledge": knowledge,
            "confidence": confidence,
            "engagement": engagement,

            "feedback": feedback,
            "recommendation": recommendation,

            "result": final
        })

    except Exception as e:
        return clean_dict({
            "success": False,
            "stage": "exception",
            "error": str(e)
        })
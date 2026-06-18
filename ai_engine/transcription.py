import whisper
from ai_engine.utils.audio_extractor import extract_audio

model = None

def get_model():
    global model
    if model is None:
        model = whisper.load_model("base")
    return model


def transcribe_video(video_path):

    try:
        audio_path = extract_audio(video_path)

        model = get_model()
        result = model.transcribe(audio_path)

        text = result.get("text", "").strip()

        return {
            "success": True,
            "transcript": text,
            "word_count": len(text.split())
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
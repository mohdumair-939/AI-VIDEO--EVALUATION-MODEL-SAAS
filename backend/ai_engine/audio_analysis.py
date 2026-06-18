import librosa
import numpy as np
from backend.ai_engine.utils.audio_extractor import extract_audio
def analyze_audio(video_path):

    try:
        audio_path = extract_audio(video_path)

        # 🔥 IMPORTANT CHECK
        if isinstance(audio_path, dict) and "error" in audio_path:
            return {"error": audio_path["error"]}

        y, sr = librosa.load(audio_path, sr=16000)

        if len(y) == 0:
            return {"error": "No audio found"}

        duration = librosa.get_duration(y=y, sr=sr)

        energy = np.abs(y)

        silent_frames = np.sum(energy < 0.02)
        total_frames = len(energy)

        silence_ratio = (silent_frames / total_frames) * 100
        speech_ratio = 100 - silence_ratio

        noise_level = np.std(y)

        return {
            "duration": float(duration),
            "silence_ratio": float(silence_ratio),
            "speech_ratio": float(speech_ratio),
            "noise_level": float(noise_level)
        }

    except Exception as e:
        return {"error": str(e)}
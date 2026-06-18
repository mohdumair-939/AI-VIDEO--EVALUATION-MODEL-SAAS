import subprocess
import os


def extract_audio(video_path, output_path="temp_audio.wav"):

    try:
        command = [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            output_path
        ]

        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return output_path

    except Exception as e:
        return {
            "error": str(e)
        }
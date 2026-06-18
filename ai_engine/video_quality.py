import cv2
import numpy as np


def check_video_quality(video_path):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return {
            "is_valid": False,
            "reason": "Cannot open video"
        }

    total_frames = 0
    blur_scores = []
    brightness_scores = []

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        total_frames += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        blur = cv2.Laplacian(gray, cv2.CV_64F).var()
        blur_scores.append(blur)

        brightness_scores.append(np.mean(gray))

    cap.release()

    if total_frames == 0:
        return {
            "is_valid": False,
            "reason": "Empty video"
        }

    avg_blur = np.mean(blur_scores)
    avg_brightness = np.mean(brightness_scores)

    is_valid = avg_blur > 20

    return {
        "is_valid": is_valid,
        "blur_score": round(avg_blur, 2),
        "brightness": round(avg_brightness, 2),
        "total_frames": total_frames
    }
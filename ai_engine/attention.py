import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)


# basic eye + nose landmark tracking
def analyze_attention(video_path):

    cap = cv2.VideoCapture(video_path)

    total_frames = 0
    focused_frames = 0
    distracted_frames = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        total_frames += 1

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:

            landmarks = results.multi_face_landmarks[0].landmark

            # key points
            nose = landmarks[1]
            left_eye = landmarks[33]
            right_eye = landmarks[263]

            # simple heuristic: compare face symmetry
            eye_diff = abs(left_eye.x - right_eye.x)

            # if eyes are aligned → likely facing front
            if eye_diff < 0.08:
                focused_frames += 1
            else:
                distracted_frames += 1

    cap.release()

    if total_frames == 0:
        return {"error": "Invalid video or no frames"}

    attention_score = (focused_frames / total_frames) * 100

    return {
        "total_frames": total_frames,
        "focused_frames": focused_frames,
        "distracted_frames": distracted_frames,
        "attention_score": round(attention_score, 2)
    }
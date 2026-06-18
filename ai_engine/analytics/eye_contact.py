import cv2
import mediapipe as mp


mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


def analyze_eye_contact(video_path):

    cap = cv2.VideoCapture(video_path)

    total_frames = 0
    eye_contact_frames = 0
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

            left_iris = landmarks[468]
            right_iris = landmarks[473]

            left_eye = landmarks[33]
            right_eye = landmarks[263]

            left_diff = abs(left_iris.x - left_eye.x)
            right_diff = abs(right_iris.x - right_eye.x)

            gaze_score = (left_diff + right_diff) / 2

            if gaze_score < 0.12:
                eye_contact_frames += 1
            else:
                distracted_frames += 1

    cap.release()

    if total_frames == 0:
        return {
            "error": "Invalid video"
        }

    eye_contact_score = (
        eye_contact_frames / total_frames
    ) * 100

    return {
        "total_frames": total_frames,
        "eye_contact_frames": eye_contact_frames,
        "distracted_frames": distracted_frames,
        "eye_contact_score": round(
            eye_contact_score,
            2
        )
    }
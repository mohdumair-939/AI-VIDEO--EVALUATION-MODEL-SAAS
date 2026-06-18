import cv2
import mediapipe as mp

mp_face = mp.solutions.face_detection
face_detector = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5)


def analyze_face(video_path):

    cap = cv2.VideoCapture(video_path)

    total = 0
    face_conf_sum = 0
    multiple_face = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        total += 1
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detector.process(rgb)

        if results.detections:
            conf = sum([d.score[0] for d in results.detections]) / len(results.detections)
            face_conf_sum += conf

            if len(results.detections) > 1:
                multiple_face += 1

    cap.release()

    if total == 0:
        return {"error": "invalid video"}

    return {
        "face_visibility": (face_conf_sum / total) * 100,
        "multiple_face_ratio": (multiple_face / total) * 100,
        "confidence": min((face_conf_sum / total) * 100, 100)
    }
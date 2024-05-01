import mediapipe as mp
import cv2

mp_face_mesh = mp.solutions.face_mesh

mp_drawing = mp.solutions.drawing_utils

drawing_spec = mp_drawing.DrawingSpec(thickness=1, color=(0, 0, 255))

face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    results = face_mesh.process(img)

    if results.multi_face_landmarks is not None:
        for res in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(img, res, mp_face_mesh.FACEMESH_TESSELATION)

    cv2.imshow('video', img)
    if cv2.waitKey(33) == 49:
        break

cap.release()
cv2.destroyAllWindows()
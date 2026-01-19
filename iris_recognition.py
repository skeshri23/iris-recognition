#iris recognition project for HACK OHI/O

import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode = False, max_num_faces = 1, refine_landmarks = True, min_detection_confidence = 0.5)

mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while(True):
    success, frame = cap.read()
    if not success:
        print("frame is not coming from the camera")
        break
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                face_landmarks,
                mp_face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec = None,
                connection_drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius = 1)
            )
        left_iris = face_landmarks.landmark[474:478]
        right_iris = face_landmarks.landmark[469:473]

        left_iris_depth = left_iris[0].z
        right_iris_depth = right_iris[0].z
        cv2.putText(frame, "Authenticated", (20, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)
        #cv2.putText(frame, "Failed to authenticate", (20, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        #cv2.putText(frame, f"left_iris_depth: {left_iris_depth}", (20, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)
        #cv2.putText(frame, f"right_iris_depth: {right_iris_depth}", (20, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("results", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()

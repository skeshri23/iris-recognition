import cv2
from iris_detector import IrisDetector

detector = IrisDetector()
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION) 

while True:
    success, frame = cap.read()
    if not success:
        break

    features = detector.extract_features(frame)

    if features is not None:
        for side in ["left", "right"]:
            cx, cy = features[f"{side}_center"].astype(int)
            radius = int(features[f"{side}_radius"])
            cv2.circle(frame, (cx, cy), radius, (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 2,      (0, 255, 0), -1)

        cv2.putText(frame, "Iris detected", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "No face detected", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("BioKey - Iris Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
import cv2
import numpy as np
import json
from iris_detector import IrisDetector

def enroll_user(name):
    detector = IrisDetector()
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

    print(f"Enrolling {name}... look at the camera. Press SPACE to capture.")

    while True:
        success, frame = cap.read()
        if not success:
            break

        cv2.imshow("BioKey - Enrollment", frame)
        key = cv2.waitKey(1)

        if key == ord(" "):
            vector = detector.get_feature_vector(frame)
            if vector is not None:
                print(f"Captured! Saving {name}'s iris template...")
                break
            else:
                print("No face detected - try again")

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save to a JSON file
    try:
        with open("templates.json", "r") as f:
            templates = json.load(f)
    except FileNotFoundError:
        templates = {}

    templates[name] = vector.tolist()

    with open("templates.json", "w") as f:
        json.dump(templates, f, indent=2)

    print(f" {name} enrolled successfully!")

enroll_user("shristi")
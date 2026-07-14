import cv2
import numpy as np
import json
from iris_detector import IrisDetector

def enroll_user(name, num_scans=5):
    detector = IrisDetector()
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

    print(f"Enrolling {name} — {num_scans} scans needed.")
    print("Press SPACE to capture each scan. Move your head slightly between scans.")

    vectors = []

    while len(vectors) < num_scans:
        success, frame = cap.read()
        if not success:
            break

        # Show progress on screen
        cv2.putText(frame, f"Scan {len(vectors)+1}/{num_scans} — press SPACE",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("BioKey - Enrollment", frame)
        key = cv2.waitKey(1)

        if key == ord(" "):
            vector = detector.get_feature_vector(frame)
            if vector is not None:
                vectors.append(vector)
                print(f"✅ Scan {len(vectors)}/{num_scans} captured")
            else:
                print("❌ No iris detected — try again")

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    if len(vectors) < num_scans:
        print("Enrollment cancelled — not enough scans captured")
        return

    # Average all scans into one robust template
    template = np.mean(vectors, axis=0)
    print(f"Template computed from {num_scans} scans")

    # Save to templates.json
    try:
        with open("templates.json", "r") as f:
            templates = json.load(f)
    except FileNotFoundError:
        templates = {}

    templates[name] = template.tolist()

    with open("templates.json", "w") as f:
        json.dump(templates, f, indent=2)

    print(f"✅ {name} enrolled successfully with {num_scans} scans!")

enroll_user("shristi")
import cv2
import numpy as np
import json
from iris_detector import IrisDetector

def load_templates():
    with open("templates.json", "r") as f:
        return {name: np.array(vector) 
                for name, vector in json.load(f).items()}

def find_match(vector, templates, threshold=120):
    best_match = None
    best_distance = float("inf")
    
    for name, template in templates.items():
        distance = np.linalg.norm(vector - template)
        if distance < best_distance:
            best_distance = distance
            best_match = name
    
    if best_distance < threshold:
        return best_match, best_distance
    return None, best_distance

def verify():
    detector = IrisDetector()
    templates = load_templates()
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    
    print("BioKey Verification — press SPACE to scan, Q to quit")
    
    while True:
        success, frame = cap.read()
        if not success:
            break
            
        cv2.imshow("BioKey - Verify", frame)
        key = cv2.waitKey(1)
        
        if key == ord(" "):
            vector = detector.get_feature_vector(frame)
            if vector is not None:
                name, distance = find_match(vector, templates)
                if name:
                    print(f" Welcome {name}! (distance: {distance:.2f})")
                else:
                    print(f" Access denied (distance: {distance:.2f})")
            else:
                print("No face detected")
                
        if key == ord("q"):
            break
    
    cap.release()
    cv2.destroyAllWindows()

verify()
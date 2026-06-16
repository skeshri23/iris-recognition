import os
os.environ["MEDIAPIPE_DISABLE_GPU"] = "1"
from flask import Flask, request, jsonify
import numpy as np
import json
import cv2
from iris_detector import IrisDetector

app = Flask(__name__)
detector = IrisDetector()

def load_templates():
    try:
        with open("templates.json", "r") as f:
            return {name: np.array(vector)
                    for name, vector in json.load(f).items()}
    except FileNotFoundError:
        return {}

def save_templates(templates):
    with open("templates.json", "w") as f:
        json.dump({name: vector.tolist()
                   for name, vector in templates.items()}, f, indent=2)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "BioKey API is running"})

@app.route("/enroll", methods=["POST"])
def enroll():
    data = request.get_json()
    name = data.get("name")
    image_path = data.get("image_path")

    if not name or not image_path:
        return jsonify({"error": "name and image_path required"}), 400

    frame = cv2.imread(image_path)
    if frame is None:
        return jsonify({"error": "could not read image"}), 400

    vector = detector.get_feature_vector(frame)
    if vector is None:
        return jsonify({"error": "no iris detected in image"}), 400

    templates = load_templates()
    templates[name] = vector
    save_templates(templates)

    return jsonify({"message": f"{name} enrolled successfully"})

@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    image_path = data.get("image_path")

    if not image_path:
        return jsonify({"error": "image_path required"}), 400

    frame = cv2.imread(image_path)
    if frame is None:
        return jsonify({"error": "could not read image"}), 400

    vector = detector.get_feature_vector(frame)
    if vector is None:
        return jsonify({"error": "no iris detected in image"}), 400

    templates = load_templates()  # reload fresh every time
    best_match = None
    best_distance = float("inf")

    for name, template in templates.items():
        distance = np.linalg.norm(vector - template)
        if distance < best_distance:
            best_distance = distance
            best_match = name

    threshold = 120
    if best_distance < threshold:
        return jsonify({
            "access": "granted",
            "identity": best_match,
            "distance": round(best_distance, 2)
        })
    else:
        return jsonify({
            "access": "denied",
            "distance": round(best_distance, 2)
        })
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
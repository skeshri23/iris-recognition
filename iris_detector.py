import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class IrisDetector:
    """
    Detects iris landmarks from a video frame and extracts
    a feature vector that can be used for identity matching.
    Uses MediaPipe FaceLandmarker (modern API, 0.10+)
    """

    # MediaPipe landmark indices for iris points
    LEFT_IRIS  = [474, 475, 476, 477]
    RIGHT_IRIS = [469, 470, 471, 472]

    def __init__(self):
        base_options = python.BaseOptions(
            model_asset_path="face_landmarker.task"
        )
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=False,
            num_faces=1
        )
        self.detector = vision.FaceLandmarker.create_from_options(options)

    def extract_features(self, frame):
        """
        Takes a single video frame and returns iris features,
        or None if no face is detected.
        """
        h, w = frame.shape[:2]

        # Convert to MediaPipe image format
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        results = self.detector.detect(mp_image)

        if not results.face_landmarks:
            return None

        landmarks = results.face_landmarks[0]

        # Convert normalized coordinates to pixel positions
        left_points = np.array([
            (landmarks[i].x * w, landmarks[i].y * h)
            for i in self.LEFT_IRIS
        ])

        right_points = np.array([
            (landmarks[i].x * w, landmarks[i].y * h)
            for i in self.RIGHT_IRIS
        ])

        # Calculate center and radius for each iris
        left_center = left_points.mean(axis=0)
        left_radius = np.linalg.norm(
            left_points - left_center, axis=1
        ).mean()

        right_center = right_points.mean(axis=0)
        right_radius = np.linalg.norm(
            right_points - right_center, axis=1
        ).mean()

        return {
            "left_center":  left_center,
            "left_radius":  left_radius,
            "right_center": right_center,
            "right_radius": right_radius,
        }
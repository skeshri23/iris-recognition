import unittest
import numpy as np
import json
import os
import cv2
import time
from iris_detector import IrisDetector

class TestIrisDetector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs once before all tests — sets up shared resources."""
        cls.detector = IrisDetector()

        # Take a real photo for testing
        cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
        time.sleep(2)
        ret, frame = cap.read()
        cap.release()
        cls.real_frame = frame

        # Create a blank black image — no face
        cls.blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)

    def test_feature_vector_length(self):
        """Vector should always have exactly 6 numbers."""
        vector = self.detector.get_feature_vector(self.real_frame)
        self.assertIsNotNone(vector)
        self.assertEqual(len(vector), 6)

    def test_no_face_returns_none(self):
        """Blank image should return None — no iris to detect."""
        vector = self.detector.get_feature_vector(self.blank_frame)
        self.assertIsNone(vector)

    def test_vector_is_numpy_array(self):
        """Output should be a numpy array, not a list or dict."""
        vector = self.detector.get_feature_vector(self.real_frame)
        self.assertIsInstance(vector, np.ndarray)

    def test_vector_all_positive(self):
        """All values should be positive — coordinates and radius."""
        vector = self.detector.get_feature_vector(self.real_frame)
        self.assertTrue(np.all(vector > 0))

    def test_same_image_same_vector(self):
        """Same image should always produce the same vector."""
        v1 = self.detector.get_feature_vector(self.real_frame)
        v2 = self.detector.get_feature_vector(self.real_frame)
        np.testing.assert_array_almost_equal(v1, v2)

    def test_radius_reasonable(self):
        """Iris radius should be between 5 and 50 pixels."""
        vector = self.detector.get_feature_vector(self.real_frame)
        left_radius = vector[2]
        right_radius = vector[5]
        self.assertGreater(left_radius, 5)
        self.assertLess(left_radius, 50)
        self.assertGreater(right_radius, 5)
        self.assertLess(right_radius, 50)

    def test_center_within_frame(self):
        """Iris centers should be within frame dimensions."""
        h, w = self.real_frame.shape[:2]
        vector = self.detector.get_feature_vector(self.real_frame)
        left_cx, left_cy = vector[0], vector[1]
        self.assertGreater(left_cx, 0)
        self.assertLess(left_cx, w)
        self.assertGreater(left_cy, 0)
        self.assertLess(left_cy, h)


class TestMatching(unittest.TestCase):

    def test_find_match_correct_identity(self):
        """Should return correct name when distance is small."""
        templates = {"shristi": np.array([100, 200, 15, 400, 210, 16])}
        query = np.array([101, 201, 15, 401, 211, 16])  # very close
        
        best_match = None
        best_distance = float("inf")
        for name, template in templates.items():
            distance = np.linalg.norm(query - template)
            if distance < best_distance:
                best_distance = distance
                best_match = name

        self.assertEqual(best_match, "shristi")
        self.assertLess(best_distance, 130)

    def test_find_match_rejects_stranger(self):
        """Should deny access when distance exceeds threshold."""
        templates = {"shristi": np.array([100, 200, 15, 400, 210, 16])}
        stranger = np.array([500, 600, 25, 800, 610, 26])  # very different

        best_distance = float("inf")
        for name, template in templates.items():
            distance = np.linalg.norm(stranger - template)
            if distance < best_distance:
                best_distance = distance

        threshold = 130
        self.assertGreater(best_distance, threshold)

    def test_templates_load_as_dict(self):
        """templates.json should load as a dictionary."""
        with open("templates.json", "r") as f:
            templates = json.load(f)
        self.assertIsInstance(templates, dict)
        self.assertGreater(len(templates), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
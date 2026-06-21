import cv2
import time
from iris_detector import IrisDetector

detector = IrisDetector()
frame = cv2.imread("shristi_fresh.jpg")

# Warm-up run (first call is always slower - model loading overhead)
detector.get_feature_vector(frame)

# Measure 10 real runs
times = []
for i in range(10):
    start = time.perf_counter()
    vector = detector.get_feature_vector(frame)
    end = time.perf_counter()
    times.append((end - start) * 1000)  # convert to milliseconds

avg_time = sum(times) / len(times)
print(f"Average processing time: {avg_time:.2f}ms")
print(f"Min: {min(times):.2f}ms, Max: {max(times):.2f}ms")
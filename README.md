# BioKey 🔑
### Iris-Based Biometric Authentication System

> "What if you never needed a key again?"

BioKey is a biometric authentication pipeline that uses your iris as your 
identity. Point a camera at your eye — BioKey enrolls you, remembers you, 
and verifies you in real time. The end goal: a hardware-attached system that 
replaces your car key entirely.

No key to forget. No key to steal. Just you.

---

## Demo

![BioKey recognizing Shristi](demo/verified.png)

*Green circles track both irises in real time. Press SPACE to authenticate.*

---

## How It Works

BioKey runs a full biometric pipeline in three stages:

**1. Detect** — MediaPipe FaceLandmarker finds 478 facial landmarks in real 
time and isolates the 8 iris points across both eyes.

**2. Extract** — The iris center coordinates and radius are computed into a 
6-number feature vector that uniquely represents that iris scan.

**3. Match** — The live feature vector is compared against enrolled templates 
using Euclidean distance. Under threshold = access granted. Over = denied.

---

## Quickstart

```bash
# Clone and set up
git clone https://github.com/skeshri23/iris-recognition
cd iris-recognition
python3 -m venv biokey-env
source biokey-env/bin/activate
pip install opencv-contrib-python mediapipe numpy

# Download the MediaPipe model
curl -o face_landmarker.task -L https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task

# Enroll yourself
python3 enroll.py

# Verify
python3 verify.py
```

---

## Results

| Scenario | Distance Score | Decision |
|----------|---------------|----------|
| Enrolled user (Shristi) | ~80 | ✅ Access Granted |
| Different person | 150–350 | ❌ Access Denied |

Threshold tuned to 120 based on real scan data.

---

## Real World Application

Cars are the obvious target — a small IR camera mounted in the door handle 
scans the driver's iris before unlocking. No physical key, no fob, no app. 
The same pipeline applies anywhere physical access needs to be controlled: 
offices, lockers, devices.

---

## Tech Stack

- Python 3.12
- MediaPipe 0.10.35 (FaceLandmarker Tasks API)
- OpenCV 4.x
- NumPy

---

## Roadmap

- [ ] Flask API — `/enroll` and `/verify` endpoints
- [ ] Web demo — try it in the browser
- [ ] Texture-based feature extraction for stronger matching
- [ ] Multi-scan enrollment for better accuracy
- [ ] Hardware prototype — Raspberry Pi + IR camera

---

## Author

Shristi Keshri — CS MEng @ University of Cincinnati  
[GitHub](https://github.com/skeshri23) | 
[LinkedIn](https://linkedin.com/in/shristikeshri2110/)
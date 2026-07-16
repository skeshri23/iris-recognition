---
title: BioKey API
emoji: 🔑
colorFrom: green
colorTo: blue
sdk: docker
sdk_version: "1.0"
app_file: app.py
pinned: false
---
# BioKey 🔑
### Iris-Based Biometric Authentication System

**Live API:** https://livewithshri-biokey-api.hf.space

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
## API

BioKey exposes a REST API so any device or app can authenticate via iris.

### Start the server
```bash
python3 api.py
# Running on http://127.0.0.1:5000
```

### Endpoints

**GET /health**
```bash
curl http://127.0.0.1:5000/health

# Response
{"status": "BioKey API is running"}
```

**POST /enroll**
```bash
curl -X POST http://127.0.0.1:5000/enroll \
  -H "Content-Type: application/json" \
  -d '{"name": "shristi", "image_path": "photo.jpg"}'

# Response
{"message": "shristi enrolled successfully"}
```

**POST /verify**
```bash
curl -X POST http://127.0.0.1:5000/verify \
  -H "Content-Type: application/json" \
  -d '{"image_path": "photo.jpg"}'

# Access granted
{"access": "granted", "identity": "shristi", "distance": 54.29}

# Access denied  
{"access": "denied", "distance": 210.82}
```

---

## Results

| Scenario | Distance | Decision |
|----------|----------|----------|
| Same image (baseline) | 0.0 | ✅ Granted |
| Same person, different photo | ~54 | ✅ Granted |
| Different person | 150–350 | ❌ Denied |

**Threshold:** 120
**Processing time:** ~15ms per scan (M1 MacBook Air, CPU only)
**Codebase:** 368 lines of Python across 6 files

> Note: FAR/FRR not yet formally measured — current threshold is based on 
> manual testing with 2 enrolled users. Formal accuracy testing with a larger 
> dataset is on the roadmap.

---

## Testing

```bash
python3 -m unittest test_biokey.py -v
```

10 unit tests covering:
- Feature vector shape and type validation
- Null detection on blank images
- Deterministic output (same image = same vector)
- Iris radius and center coordinate bounds
- Matching logic for known users and strangers
- Template persistence

All 10 passing ✅

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
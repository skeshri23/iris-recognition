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

# BioKey
**Iris-Based Biometric Authentication System**

> Started as a hackathon script. Became a deployed authentication system.

BioKey uses your iris as your identity. Look at a camera, press verify — 
BioKey tells you who you are and whether to grant access. The end vision: 
a small IR camera on your car door handle that replaces your key entirely.

No key to forget. No key to steal. Just you.

**[Try it live →](https://livewithshri-biokey-api.hf.space)**

---

## Demo

![BioKey Demo](demo/biokey_demo.gif)

---

## How It Works

BioKey runs a three-stage biometric pipeline:

**1. Detect** — MediaPipe FaceLandmarker locates 478 facial landmarks in 
real time, isolating 8 iris points across both eyes.

**2. Extract** — Iris center coordinates and radius are computed into a 
6-number feature vector representing that specific iris scan.

**3. Match** — The live vector is compared against enrolled templates using 
Euclidean distance. Under threshold → access granted. Over → denied.

---

## Results

| Scenario | Distance | Decision |
|----------|----------|----------|
| Same image (baseline) | 0.0 | Granted |
| Same person, different photo | ~54 | Granted |
| Different person | 150-350 | Denied |

- Threshold: 130
- Processing time: ~15ms per scan (M1 MacBook Air, CPU only)
- Codebase: 368 lines of Python across 6 files
- Unit tests: 10 passing

> FAR/FRR not yet formally measured — threshold tuned empirically 
> with 2 enrolled users. Formal accuracy testing is on the roadmap.

---

## Quickstart

**Prerequisites:** Python 3.12, a webcam

```bash
# Clone
git clone https://github.com/skeshri23/iris-recognition
cd iris-recognition

# Set up environment
python3 -m venv biokey-env
source biokey-env/bin/activate  # Mac/Linux
# biokey-env\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Download MediaPipe model
curl -L -o face_landmarker.task \
  https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task

# Start the web app
python3 app.py

# Open in browser
# http://localhost:7860
```

**Mac:** If camera doesn't open, disconnect iPhone Continuity Camera 
or set `cv2.CAP_AVFOUNDATION` in `app.py`.

**Windows:** Change `CAP_AVFOUNDATION` to `cv2.CAP_DSHOW` in `app.py`.

---

## API

Five endpoints available. Run `python3 app.py` to start locally.

**GET /health**
```bash
curl http://localhost:7860/health
# {"status": "BioKey API is running"}
```

**POST /enroll** — register a user via image file
```bash
curl -X POST http://localhost:7860/enroll \
  -H "Content-Type: application/json" \
  -d '{"name": "shristi", "image_path": "photo.jpg"}'
# {"message": "shristi enrolled successfully"}
```

**POST /verify** — verify identity via image file
```bash
curl -X POST http://localhost:7860/verify \
  -H "Content-Type: application/json" \
  -d '{"image_path": "photo.jpg"}'
# {"access": "granted", "identity": "shristi", "distance": 54.29}
```

**POST /enroll_base64** — enroll via browser webcam frame

**POST /verify_base64** — verify via browser webcam frame

---

## Testing

```bash
python3 -m unittest test_biokey.py -v
```

10 tests covering feature vector validation, null detection on blank 
images, deterministic output, iris radius and coordinate bounds, 
matching logic, and template persistence. All passing.

---

## Real World Applications

The same pipeline applies anywhere physical access needs to be controlled:

- Car door unlock — IR camera in the door handle, no key needed
- Office access control — replace keycards
- Device unlock — more secure than face ID
- Hospital patient verification — no credential to lose or steal

---

## Tech Stack

- Python 3.12
- MediaPipe 0.10.35 (FaceLandmarker Tasks API)
- OpenCV 4.x
- Flask
- NumPy
- Docker

---

## Roadmap

- [x] Real-time iris detection pipeline
- [x] Feature extraction and Euclidean matching
- [x] Multi-scan enrollment (5-scan average)
- [x] Flask REST API
- [x] Browser-based webcam UI
- [x] Docker deployment on Hugging Face Spaces
- [x] 10 unit tests
- [ ] Texture-based feature extraction (Gabor filters)
- [ ] Formal FAR/FRR testing with larger dataset
- [ ] Hardware prototype — Raspberry Pi + IR camera

---

## Author

Shristi Keshri — CS @ Ohio State | MEng CS @ University of Cincinnati
[GitHub](https://github.com/skeshri23) | [LinkedIn](https://linkedin.com/in/shristikeshri2110)
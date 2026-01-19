# Iris Recognition for Keyless Car Unlocking

## Overview
This project implements a real-time iris recognition pipeline developed during the
HACKOHI/O hackathon. The system focuses on detecting and processing eye regions from
live video input to enable biometric authentication.

The project was later refined to explore robustness, preprocessing, and real-time
computer vision performance.

---

## Problem Statement
Traditional key-based vehicle access systems are vulnerable to theft and misuse.
This project explores iris-based biometric authentication as a secure, contactless
alternative for keyless car unlocking.

---

## Approach
- Capture live video input
- Detect facial landmarks and eye regions
- Isolate iris region using computer vision techniques
- Apply preprocessing for lighting normalization
- Perform feature extraction for authentication

---

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt

   python iris_recognition.py

---

## Technologies Used
- Python
- OpenCV
- MediaPipe

---

## Project Context
Built as part of the **HACKOHI/O Hackathon** and extended independently to deepen
understanding of real-time computer vision pipelines and biometric security systems.

---

## Limitations & Future Work
- Improve robustness under extreme lighting conditions
- Integrate a trained iris matching model
- Optimize performance for embedded systems

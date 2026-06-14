# What I Built & What I Learned

## BioKey — Session by Session

### Session 1 — Iris Detection
- **What I built:** IrisDetector class that finds both irises in real time
- **What I learned:**
  - `__init__` runs automatically when you create an object — it's construction instructions
  - MediaPipe gives 478 face landmarks normalized between 0-1 — multiply by frame width/height to get pixels
  - A feature vector is just a list of numbers that describes something measurable
  - `np.linalg.norm` calculates distance between two points using Pythagorean theorem

### Session 2 — Feature Extraction
- **What I built:** `get_feature_vector()` — flattens iris data into 6 numbers
- **What I learned:**
  - `np.concatenate` joins multiple arrays into one flat array
  - A flat array is better than a dictionary for math operations and file storage
  - Classes hold state between calls — functions can't do that

### Session 3 — Enrollment
- **What I built:** `enroll.py` — captures iris from webcam and saves to templates.json
- **What I learned:**
  - `try/except` handles errors gracefully — don't crash if file doesn't exist
  - JSON stores data as key-value pairs — human readable, easy to load/save
  - `vector.tolist()` converts numpy array to plain Python list for JSON serialization

### Session 4 — Verification
- **What I built:** `verify.py` — compares live iris against stored templates
- **What I learned:**
  - Euclidean distance measures how similar two vectors are
  - A threshold is the cutoff between "close enough to match" and "too different"
  - Biometric templates drift with lighting — same person, different conditions = higher distance
  - Tuning threshold is real biometric engineering work

### Session 5 — Flask API
- **What I built:** `api.py` — REST API with /health, /enroll, /verify
- **What I learned:**
  - A REST API lets any device call your code over HTTP
  - `@app.route` is a decorator — it tells Flask which URL triggers which function
  - APIs should reload data fresh on every request, not cache it at startup
  - Camera needs warmup time — `time.sleep(2)` before capturing fixes black frames

---

## Interview Questions I Can Answer

**"What is BioKey?"**
BioKey is a biometric authentication pipeline that uses iris recognition to 
verify identity. It detects iris landmarks using MediaPipe, extracts a 6-number 
feature vector representing each iris, and compares live scans against enrolled 
templates using Euclidean distance. It exposes a Flask REST API so any device 
can authenticate via HTTP.

**"What challenges did you face?"**
Iris feature vectors are sensitive to lighting and camera position. I discovered 
that templates enrolled under different conditions would drift, causing 
misidentification. I solved this by ensuring enrollment and verification happen 
under consistent conditions, and plan to fix it properly with multi-scan 
averaging. I also hit MediaPipe's breaking API change from 0.9 to 0.10 and had 
to migrate the entire codebase to the new Tasks API.

**"What is a feature vector?"**
A feature vector is a list of numbers that describes something measurable about 
an object. For BioKey, it's 6 numbers: left iris center x, left iris center y, 
left iris radius, right iris center x, right iris center y, right iris radius. 
Two similar irises will have similar vectors — small distance between them. 
Two different irises will have large distance.

**"Why Euclidean distance?"**
Euclidean distance measures how far apart two points are in multi-dimensional 
space — it's the Pythagorean theorem generalized to N dimensions. For our 6-number 
vectors, it gives a single number representing how different two iris scans are. 
Simple, fast, interpretable. A production system would use more sophisticated 
matching but this demonstrates the core concept clearly.

**"What would you improve?"**
Three things: first, multi-scan enrollment — average 5 scans instead of 1 to 
create a more robust template. Second, texture-based features using Gabor filters 
on the iris region for stronger discrimination. Third, deploy the Flask API so 
it's accessible over the internet, not just localhost.

**"What is a REST API?"**
A REST API is a way for different programs to talk to each other over HTTP. 
BioKey's API has three endpoints: /health checks if the server is running, 
/enroll saves a new user's iris template, and /verify checks if a live scan 
matches any enrolled user. Any device — a web app, mobile app, or Raspberry Pi 
on a car door — can call these endpoints.
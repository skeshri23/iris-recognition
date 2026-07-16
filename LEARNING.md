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

### Session 6 — Deployment

- **What I built:** Deployed BioKey as a live API on Hugging Face Spaces
- **Live URL:** https://livewithshri-biokey-api.hf.space

- **What I learned:**
  - Docker packages your entire app — code, dependencies, system libraries — into one portable container that runs the same everywhere
  - `FROM python:3.12-slim` starts with a minimal Linux image with Python pre-installed
  - `RUN apt-get install` installs system libraries (like OpenGL) that Python packages depend on
  - `EXPOSE 7860` tells Docker which port the app listens on
  - `ENV PORT=7860` sets an environment variable inside the container
  - Hugging Face Spaces uses port 7860 by default — not 5000
  - MediaPipe needs libGL, libEGL, and libGLES to run on headless Linux servers
  - `python:3.12-slim` doesn't include curl — you have to install it explicitly
  - Deployment is always harder than it looks — even senior engineers spend hours on this

- **Challenges I solved:**
  - Railway free tier ran out mid-deploy
  - Render blocked system package installation
  - Wrong OpenGL package names across different Debian versions
  - Binary files rejected by Hugging Face git — purged from history with `git filter-branch`
  - Token authentication with special characters breaking zsh URL parsing

  ### Session 7 — Multi-scan enrollment

- **What I built:** Updated enrollment to capture 5 scans and average them
- **What I learned:**
  - A single scan is noisy — lighting, angle, distance all shift the vector
  - Averaging multiple scans smooths out noise and gives a more robust template
  - `np.mean(vectors, axis=0)` averages each of the 6 numbers across all scans
  - Threshold tuning is iterative — 120 was too tight after multi-scan, 130 works
  - Distance 106 on a real verification = healthy margin below threshold

### Session 8 — Unit Testing

- **What I built:** 10 unit tests covering the full BioKey pipeline
- **What I learned:**
  - `unittest` is Python's built-in testing framework
  - `setUpClass` runs once before all tests — use it for expensive setup like loading ML models
  - `assertEqual`, `assertIsNone`, `assertGreater` — assertions are how you check expected vs actual
  - `np.testing.assert_array_almost_equal` compares numpy arrays with floating point tolerance
  - Tests catch regressions — if you change code and break something, tests tell you immediately
  - A blank black image is a good edge case test — real systems must handle bad input gracefully

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

**"Have you deployed anything?"**
Yes — BioKey's Flask API is live at https://livewithshri-biokey-api.hf.space, 
deployed on Hugging Face Spaces using Docker. I wrote a Dockerfile that installs 
OpenGL system dependencies, downloads the MediaPipe model, and starts the Flask 
server on port 7860.

**"What is Docker?"**
Docker packages an application and everything it needs — code, runtime, system 
libraries, dependencies — into a container that runs consistently anywhere. 
Instead of "it works on my machine," Docker makes it work on every machine. 
I used it to deploy BioKey because MediaPipe requires specific OpenGL libraries 
that aren't available by default on cloud servers.

**"What challenges did you face in deployment?"**
MediaPipe 0.10+ requires OpenGL libraries (libGL, libEGL, libGLES) that aren't 
pre-installed on headless Linux servers. I tried Render and Railway first but hit 
platform limitations. I eventually deployed on Hugging Face Spaces using Docker, 
manually installing the exact OpenGL packages needed for Debian trixie. I also 
had to purge a binary file from git history using git filter-branch when Hugging 
Face rejected the push.

**"What's your processing time / accuracy?"**
Processing takes about 15ms per scan on a MacBook Air M1, CPU only — well 
under real-time requirements. I haven't run formal FAR/FRR testing yet since 
I only have 2 enrolled users; that's explicitly on my roadmap before I'd call 
this production-ready. The threshold of 120 was tuned empirically — same-person 
scans cluster at 50-100 distance, different-person scans are consistently 150+.

**"Why did you add multi-scan enrollment?"**
A single iris scan is sensitive to lighting and head position — small changes 
shift the feature vector. Averaging 5 scans smooths out that noise, giving a 
more stable template. After switching to multi-scan, same-person distances 
became more consistent and I could set a tighter threshold with more confidence.

**"Do you write tests?"**
Yes — BioKey has 10 unit tests covering feature extraction, null handling, 
matching logic, and data validation. I used Python's unittest framework with 
setUpClass to load the MediaPipe model once and reuse it across tests. 
All 10 pass in under 5 seconds.
FROM python:3.12-slim

# Install OpenGL dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libgles2-mesa \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Download the MediaPipe model
RUN curl -L -o face_landmarker.task \
    https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task

COPY . .

EXPOSE 7860

ENV PORT=7860

CMD ["python", "app.py"]
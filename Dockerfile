FROM python:3.12-slim

# System dependencies for OpenCV + YOLO
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency manifest first (layer cache)
COPY pyproject.toml .

# Install Python dependencies (no venv needed inside Docker)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    "vision-agents[gemini,getstream,ultralytics]>=0.3.8" \
    "python-dotenv>=1.0.0" \
    "fastapi>=0.115.0" \
    "uvicorn[standard]>=0.34.0" \
    "pyjwt>=2.9.0"

# Copy source code
COPY main.py .
COPY server.py .
COPY sports_processor.py .
COPY instructions.md .
COPY yolo11n-pose.pt .
COPY start.sh .

RUN chmod +x start.sh

# Cloud Run sets PORT env var (default 8080)
ENV PORT=8080

EXPOSE 8080

CMD ["./start.sh"]

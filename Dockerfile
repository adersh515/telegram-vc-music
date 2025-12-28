FROM python:3.11-slim

# System dependencies for tgcalls
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    build-essential \
    cmake \
    libssl-dev \
    libopus-dev \
    libsrtp2-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install pytgcalls + tgcalls from GitHub (MATCHING v2.0.0)
RUN pip install --no-cache-dir \
    git+https://github.com/pytgcalls/tgcalls.git@v2.0.0 \
    git+https://github.com/pytgcalls/pytgcalls.git@v2.0.0

COPY . .

CMD ["python", "main.py"]

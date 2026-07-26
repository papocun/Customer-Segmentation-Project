# -------------------------------
# Base Image
# -------------------------------
FROM python:3.11-slim

# -------------------------------
# Environment Variables
# -------------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -------------------------------
# Working Directory
# -------------------------------
WORKDIR /app

# -------------------------------
# Install System Dependencies
# -------------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Copy Entire Project
# -------------------------------
COPY . /app

# -------------------------------
# Upgrade pip
# -------------------------------
RUN pip install --upgrade pip

# -------------------------------
# Install Python Dependencies
# -------------------------------
RUN pip install -r requirements.txt

# -------------------------------
# Install Project
# -------------------------------
RUN pip install .

# -------------------------------
# Expose Ports
# -------------------------------
EXPOSE 8000
EXPOSE 8501

# -------------------------------
# Default Command
# (docker-compose overrides this)
# -------------------------------
CMD ["bash"]
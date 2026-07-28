#!/bin/bash
# ==============================================================================
# AWS EC2 Automated Deployment Script for Customer Segmentation App
# ==============================================================================
# This script installs Docker, Docker Compose, clones the repository, and
# launches the application using Docker Compose.
# Suitable for AWS EC2 User Data script or running directly on Ubuntu/Debian EC2.
# ==============================================================================

set -e

echo "🚀 Starting AWS EC2 Setup & Deployment..."

# 1. Update package list and install system prerequisites
sudo apt-get update -y
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common git

# 2. Install Docker
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    sudo systemctl enable docker
    sudo systemctl start docker
else
    echo "✅ Docker is already installed."
fi

# 3. Install Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "📦 Installing Docker Compose..."
    sudo apt-get install -y docker-compose-plugin
fi

# 4. Clone or Pull Latest Code
REPO_DIR="/home/ubuntu/Customer-Segmentation-Project"
REPO_URL="https://github.com/papocun/Customer-Segmentation-Project.git"

if [ -d "$REPO_DIR" ]; then
    echo "🔄 Pulling latest changes into $REPO_DIR..."
    cd "$REPO_DIR"
    git pull origin main
else
    echo "📥 Cloning repository from GitHub..."
    git clone "$REPO_URL" "$REPO_DIR"
    cd "$REPO_DIR"
fi

# 5. Launch Docker Compose Services
echo "🐳 Building and starting Docker containers..."
sudo docker compose up -d --build

# 6. Success Output
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 || echo "<EC2_PUBLIC_IP>")
echo "=================================================================="
echo "🎉 DEPLOYMENT COMPLETE!"
echo "🌐 Frontend URL (Streamlit): http://${PUBLIC_IP}:8501"
echo "⚙️ Backend API (FastAPI):   http://${PUBLIC_IP}:8000"
echo "=================================================================="

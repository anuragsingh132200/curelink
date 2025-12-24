#!/bin/bash

# Disha AI Health Coach - Startup Script

echo "======================================"
echo "Disha AI Health Coach"
echo "======================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo ""
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your API keys:"
    echo "   - GEMINI_API_KEY or OPENAI_API_KEY"
    echo ""
    read -p "Press Enter to continue once you've added your API keys..."
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running!"
    echo "Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: docker-compose not found!"
    echo "Please install Docker Compose and try again."
    exit 1
fi

echo "🐳 Starting Docker containers..."
echo ""

# Start docker-compose
docker-compose up --build

# This will keep running until Ctrl+C

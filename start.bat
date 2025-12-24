@echo off
REM Disha AI Health Coach - Windows Startup Script

echo ======================================
echo Disha AI Health Coach
echo ======================================
echo.

REM Check if .env exists
if not exist .env (
    echo Error: .env file not found!
    echo.
    echo Creating .env from .env.example...
    copy .env.example .env
    echo .env file created
    echo.
    echo IMPORTANT: Please edit .env and add your API keys:
    echo    - ANTHROPIC_API_KEY or OPENAI_API_KEY
    echo.
    pause
)

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo Starting Docker containers...
echo.

REM Start docker-compose
docker-compose up --build

pause

@echo off
echo 🚀 Starting Customer Support Bot - LLM Comparison Tool
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  No .env file found. Please copy env.example to .env and configure your API keys.
    echo    copy env.example .env
    echo    Then edit .env with your API keys and run this script again.
    pause
    exit /b 1
)

REM Start the application
echo 🌐 Starting the application...
echo 📖 API docs will be available at: http://localhost:8000/docs
echo 💬 Chat interface will be available at: http://localhost:8000/
echo 🛑 Press Ctrl+C to stop the server
echo.

python main.py
pause

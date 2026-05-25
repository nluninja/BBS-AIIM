@echo off
REM Startup script for Cornwall Travel Assistant Web UI (Windows)

echo 🏖️ Starting Cornwall Travel Assistant Web UI...

REM Check if virtual environment exists
if not exist "myagent" (
    echo ❌ Virtual environment 'myagent' not found!
    echo Please run setup first:
    echo   python -m venv myagent
    echo   myagent\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo ❌ .env file not found!
    echo Please create .env file with your OpenAI API key:
    echo   copy .env.example .env
    echo   REM Edit .env and add your OPENAI_API_KEY
    pause
    exit /b 1
)

REM Activate virtual environment and run Streamlit
echo 🚀 Activating environment and starting web UI...
call myagent\Scripts\activate
streamlit run app.py --server.port 8501 --server.address localhost
pause
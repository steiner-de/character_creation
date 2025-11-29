@echo off
REM Create and activate virtual environment for Windows (batch)

if exist venv (
    echo Virtual environment already exists.
) else (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Virtual environment activated!
echo Installing dependencies...
pip install -r requirements.txt

echo Setup complete! Virtual environment is ready.

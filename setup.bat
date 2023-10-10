@echo off
REM Check if venv exists, if not create it
IF NOT EXIST "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Install dependencies
pip install selenium requests pyinstaller

REM Create the executable
pyinstaller --onefile TT_No_Watermark.py

REM Deactivate the virtual environment
call venv\Scripts\deactivate.bat

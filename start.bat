@echo off
ECHO Activating virtual environment...
CALL venv\Scripts\activate.bat

ECHO.
ECHO Starting the Safety Detector...
python main.py

ECHO.
ECHO Script finished. Press any key to exit.
PAUSE
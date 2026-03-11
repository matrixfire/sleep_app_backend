@echo off
REM This script automates the setup and startup of the sleep_app_backend project.

setlocal EnableExtensions EnableDelayedExpansion

REM Ensure we run from this script's directory.
cd /d "%~dp0"

REM Ensure the virtual environment exists.
if not exist ".\.venv\Scripts\python.exe" (
    ECHO [. ] Creating virtual environment at .venv...
    py -3 -m venv .venv
    IF %ERRORLEVEL% NEQ 0 (
        ECHO.
        ECHO ERROR: Failed to create venv. Ensure Python is installed and the "py" launcher works.
        ECHO Tip: Try running: py -3 --version
        PAUSE
        EXIT /B 1
    )
)

ECHO [1/3] Installing dependencies from requirements.txt...
REM Ensure all required Python packages are installed in the virtual environment.
call .\.venv\Scripts\python.exe -m pip install --upgrade pip
call .\.venv\Scripts\python.exe -m pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    ECHO.
    ECHO ERROR: Failed to install dependencies. Please check your internet connection and requirements.txt.
    PAUSE
    EXIT /B 1
)

ECHO.
ECHO [2/3] Initializing the database...
REM This script creates database tables and a default admin user.
call .\.venv\Scripts\python.exe -m app.scripts.init_db
IF %ERRORLEVEL% NEQ 0 (
    ECHO.
    ECHO ERROR: Failed to initialize the database. Please check your .env file and ensure the database server is running.
    PAUSE
    EXIT /B 1
)

ECHO.
ECHO [3/3] Starting the Uvicorn server...
REM The server will run and reload automatically on code changes.
call .\.venv\Scripts\uvicorn.exe main:app --host 0.0.0.0 --port 8000 --reload

ECHO.
ECHO Server has been stopped.
PAUSE

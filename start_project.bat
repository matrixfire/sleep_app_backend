@echo off
REM This script automates the setup and startup of the sleep_app_backend project.

ECHO [1/3] Installing dependencies from requirements.txt...
REM Ensure all required Python packages are installed in the virtual environment.
call .\.venv\Scripts\pip.exe install -r requirements.txt
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

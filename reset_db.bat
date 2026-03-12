@echo off
REM Reset DB: remove MySQL container + volume, recreate container, run init_db.
REM Run this from project root. After it finishes, start the API with start_project.bat or uvicorn.

setlocal EnableExtensions

cd /d "%~dp0"

echo [1/5] Stopping and removing MySQL container...
docker rm -f sleep-mysql 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Container may not exist; continuing.
)

echo.
echo [2/5] Removing MySQL data volume...
docker volume prune -f

echo.
echo [3/5] Starting fresh MySQL container...
docker run -d --name sleep-mysql ^
  -e MYSQL_ROOT_PASSWORD=password ^
  -e MYSQL_DATABASE=sleep_app ^
  -p 3306:3306 ^
  mysql:8.0
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to start MySQL container. Is Docker Desktop running?
    pause
    exit /b 1
)

echo.
echo [4/5] Waiting for MySQL to be ready (about 25 seconds)...
timeout /t 25 /nobreak >nul

echo.
echo [5/5] Creating tables and seeding admin user...
if not exist ".\.venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found. Run: python -m venv .venv
    pause
    exit /b 1
)
call .\.venv\Scripts\python.exe -m app.scripts.init_db
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: init_db failed. Check .env and try again.
    pause
    exit /b 1
)

echo.
echo Done. Database reset complete. Run start_project.bat to start the API.
pause

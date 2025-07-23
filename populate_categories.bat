@echo off
rem This batch file runs the Django management command to populate categories.

rem --- IMPORTANT: Configure these paths ---
set VENV_PATH="C:\Users\ibito\Documents\Django_Class\venv"
set PROJECT_ROOT="C:\Users\ibito\Documents\Django_Class"
rem ---------------------------------------

echo Activating virtual environment...
call "%VENV_PATH%\Scripts\activate.bat"

if %ERRORLEVEL% NEQ 0 (
    echo Error: Could not activate virtual environment. Check VENV_PATH.
    pause
    exit /b %ERRORLEVEL%
)

echo Changing to project r  oot directory: %PROJECT_ROOT%
cd /d "%PROJECT_ROOT%"

if %ERRORLEVEL% NEQ 0 (
    echo Error: Could not change to project directory. Check PROJECT_ROOT.
    pause
    exit /b %ERRORLEVEL%
)

echo Running Django populate_categories command...
python manage.py populate_categories

if %ERRORLEVEL% NEQ 0 (
    echo Error: Django command failed. See above for details.
) else (
    echo Django command completed successfully.
)

pause

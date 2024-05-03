@echo off

REM Check if Python is installed
where python > nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed.
    echo Please install Python and run this script again.
    exit /b 1
)

REM Check Python version
for /f "tokens=2 delims=." %%a in ('python --version 2^>^&1') do set PYTHON_VERSION=%%a
set REQUIRED_PYTHON_VERSION=3.6

if "%PYTHON_VERSION%" lss "%REQUIRED_PYTHON_VERSION%" (
    echo Error: Python %REQUIRED_PYTHON_VERSION% or higher is required
    exit /b 1
)

REM Check if cryptography is installed
python -c "import cryptography" > nul 2>&1
if errorlevel 1 (
    echo Installing cryptography...
    python -m pip install cryptography || (
        echo Error: Failed to install cryptography
        exit /b 1
    )
)

REM Check if pywin32 is installed
python -c "import win32api" > nul 2>&1
if errorlevel 1 (
    echo Installing pywin32...
    python -m pip install pywin32 || (
        echo Error: Failed to install pywin32
        exit /b 1
    )
)

REM Create directory "SecureScribe"
mkdir "C:\Program Files\SecureScribe" > nul

REM Copy Python script
copy "SecureScribe_V2.py" "C:\Program Files\SecureScribe\SecureScribe_V2.py" > nul

REM Create logging directory
mkdir "C:\Program Files\SecureScribe\ScribeLogs" > nul

echo Installation completed.
echo You can now run your script.

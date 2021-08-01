@echo off
python --version >nul 2>&1
if errorlevel 1 (
  echo [x] Python is not installed >&2
  exit /b
)

echo [+] Found Python

python --version | findstr /R "[3]\.[7-9]" >nul 2>&1
if errorlevel 1 (
  echo [x] The minimum required version of python is python3.7 >&2
  exit /b
)

python -m pip -V >nul
if errorlevel 1 (
  echo [x] pip not found >&2
  exit /b
)

echo [+] Found pip
echo [*] Running pip upgrade...
python -m pip install --no-cache-dir --upgrade pip

echo [*] Creating a virtual environment...
rmdir "venv" /q /s >nul 2>&1
python -m venv --clear .\venv
if errorlevel 1 (
  echo [x] Failed to create a virtual environment >&2
  exit /b
)

set pythonvenv=.\venv\Scripts\python.exe
%pythonvenv% -m pip install --upgrade pip

echo [*] Installing the prerequisites...
%pythonvenv% -m pip install --no-cache-dir -r requirements.txt

if errorlevel 1 (
  echo [x] Installation failed >&2
  exit /b
)

echo [+] Installation complete!
exit /b 0

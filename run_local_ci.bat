@echo off
echo Starting Local CI Security Pipeline...
echo 325325325325325325325325325325325325

echo.
echo [1/2] Running SAST (Bandit)...
call venv\Scripts\activate
bandit app.py
if %errorlevel% neq 0 (
    echo SAST Failed!
    exit /b %errorlevel%
)

echo.
echo [2/2] Running SCA (pip-audit)...
pip-audit
if %errorlevel% neq 0 (
    echo SCA Failed!
    exit /b %errorlevel%
)

echo.
echo 325325325325325325325325325325325325
echo CI Pipeline Completed Successfully!
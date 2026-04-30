@echo off

echo =========================================
echo 1. Starting creation and deployment (clientDns.py)...
echo =========================================
python clientDns.py

REM Error checking for the first script
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] A problem occurred with clientDns.py. Aborting.
    exit /b %ERRORLEVEL%
)

echo.
echo [SUCCESS] clientDns deployment completed!
echo.
echo Press any key when you have finished testing and are ready for the UNDEPLOY of the first lab...
pause >nul

echo =========================================
echo 2. Starting undeploy of the first lab...
echo =========================================
python clientUndeployDns.py
echo Undeploy completed.
echo.

echo =========================================
echo 3. Starting V2 creation and deployment (clientDns2.0.py)...
echo =========================================
python clientDns2.0.py

REM Error checking for the second script
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] A problem occurred with clientDns2.0.py. Aborting.
    exit /b %ERRORLEVEL%
)

echo.
echo [SUCCESS] clientDns2.0 deployment completed!
echo.
echo Press any key when you have finished testing and are ready for the FINAL UNDEPLOY...
pause >nul

echo =========================================
echo 4. Starting final undeploy of the lab...
echo =========================================
python clientUndeployDns.py

echo.
echo =========================================
echo All operations completed successfully!
echo =========================================
pause
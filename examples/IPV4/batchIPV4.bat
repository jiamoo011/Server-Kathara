@echo off
echo =========================================
echo Starting lab creation and deployment...
echo =========================================
python clientIPV4.py

if %ERRORLEVEL% NEQ 0 (
    echo An error occurred during lab creation. Aborting.
    exit /b %ERRORLEVEL%
)

echo.
echo Deployment completed successfully!
echo.

echo Press any key when you are ready to undeploy the lab...
pause >nul

echo =========================================
echo Starting lab undeploy...
echo =========================================
python clientUndeployIPV4.py

echo Operation completed.
@echo off
echo =========================================
echo Avvio della creazione e del deploy del lab...
echo =========================================
python clientIPV4.py

if %ERRORLEVEL% NEQ 0 (
    echo Si e' verificato un errore durante la creazione del lab. Interruzione.
    exit /b %ERRORLEVEL%
)

echo.
echo Deploy completato con successo!
echo.

echo Premi un tasto quando sei pronto per eseguire l'undeploy del lab...
pause >nul

echo =========================================
echo Avvio dell'undeploy del lab...
echo =========================================
python clientUndeployIPV4.py

echo Operazione completata.
@echo off
:loop
echo %date% %time% starting IanETrading…
python -m src.main_realtime
if %errorlevel% neq 0 (
    echo %date% %time% crashed; restarting in 5 seconds…
    timeout /t 5 /nobreak >nul
    goto loop
)
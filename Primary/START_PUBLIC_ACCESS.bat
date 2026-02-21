@echo off
title Primary Learn Hub - Public Access
echo ==========================================
echo   Generating Public URL (LocalTunnel)
echo ==========================================
echo.
echo [1] Starting Streamlit in the background...
start /b streamlit run app.py --server.port 8501
echo.
echo [2] Launching Public URL Generator...
echo.
echo ------------------------------------------
echo IMPORTANT: When the website opens, it may ask for a "Tunnel Password".
echo If it does, use the IP address shown in your terminal or '34.125.42.222'.
echo ------------------------------------------
echo.
npx localtunnel --port 8501
pause

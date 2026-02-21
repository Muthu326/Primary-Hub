@echo off
title Primary Learn Hub - Local Network
echo ==========================================
echo   Starting Primary Learn Hub (Local Network)
echo ==========================================
echo.
echo Anyone on your WiFi can access the app using your IP address.
echo Look for the "Network URL" below after Streamlit starts.
echo.
streamlit run app.py --server.address 0.0.0.0
pause

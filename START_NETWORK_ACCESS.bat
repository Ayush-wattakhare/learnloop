@echo off
echo ========================================
echo   LearnLoop - Network Access Mode
echo ========================================
echo.
echo Starting LearnLoop for network access...
echo.
echo Your app will be accessible from:
echo   - This computer: http://127.0.0.1:5000
echo   - Other devices: http://YOUR_IP:5000
echo.
echo To find your IP address, look below:
echo.
ipconfig | findstr /i "IPv4"
echo.
echo Share the IP address above with others on the same WiFi!
echo.
echo ========================================
echo   Starting application...
echo ========================================
echo.
python app.py
pause

@echo off
cls
echo ============================================================
echo   LearnLoop - Starting Application
echo ============================================================
echo.
echo Checking database connection...
python test_connection.py
echo.
echo ============================================================
echo   Starting Flask Server with Voice Rooms
echo ============================================================
echo.
echo Server will start on: http://127.0.0.1:5000
echo.
echo Features Available:
echo   - User Registration and Login
echo   - Find Study Partners
echo   - Study Groups
echo   - Group Chat
echo   - Notes Sharing
echo   - Voice Rooms (NEW!)
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.
python app.py
pause

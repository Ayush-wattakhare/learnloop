@echo off
echo ============================================================
echo   LearnLoop - Complete Feature Check and Startup
echo ============================================================
echo.

echo Step 1: Testing Database Connection...
python test_all_features.py
echo.

if errorlevel 1 (
    echo ❌ Database test failed!
    echo Please check your MySQL connection and try again.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   All Features Connected Successfully!
echo ============================================================
echo.
echo Starting Flask Server...
echo.
echo Server will be available at: http://127.0.0.1:5000
echo.
echo Features Available:
echo   ✅ User Registration and Login
echo   ✅ Profile with Picture Upload
echo   ✅ Find Study Partners (by Topic and Language)
echo   ✅ Friend Requests and Messaging
echo   ✅ File Sharing (Images, PDFs, Documents)
echo   ✅ Voice Call (UI Ready)
echo   ✅ Study Groups with Chat
echo   ✅ Notes Sharing
echo   ✅ Voice Rooms with Whiteboard
echo   ✅ View User Profiles
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python app.py

# 🚀 How to Run LearnLoop Project

## Quick Start (3 Methods)

---

## Method 1: Double-Click Launcher (Easiest) ⭐

### Step 1: Double-click the file
```
RUN_PROJECT.bat
```

### Step 2: Wait for server to start
You'll see:
```
* Running on http://127.0.0.1:5000
```

### Step 3: Open your browser
```
http://127.0.0.1:5000
```

**That's it!** 🎉

---

## Method 2: Command Line

### Step 1: Open Command Prompt or PowerShell
- Press `Win + R`
- Type `cmd` or `powershell`
- Press Enter

### Step 2: Navigate to project folder
```bash
cd C:\Users\ASUS\Downloads\LearnLoop
```

### Step 3: Run the application
```bash
python app.py
```

### Step 4: Open browser
```
http://127.0.0.1:5000
```

---

## Method 3: With Virtual Environment

### Step 1: Activate virtual environment
```bash
.venv\Scripts\activate
```

### Step 2: Run application
```bash
python app.py
```

### Step 3: Open browser
```
http://127.0.0.1:5000
```

---

## 📱 Access from Mobile/Tablet

### Step 1: Find your computer's IP address
```bash
ipconfig
```
Look for "IPv4 Address" (e.g., 192.168.1.100)

### Step 2: Make sure mobile is on same WiFi

### Step 3: Open browser on mobile
```
http://YOUR_IP:5000
Example: http://192.168.1.100:5000
```

---

## ✅ Verify Everything is Working

### 1. Check Database Connection
```bash
python test_connection.py
```

Expected output:
```
✅ Connection successful!
✅ Connected to database: learnloop
📊 Found 10 tables
```

### 2. Check Dependencies
```bash
pip list | findstr -i "flask mysql socket"
```

Expected output:
```
Flask         3.1.2
Flask-MySQLdb 2.0.0
flask-socketio 5.6.0
mysqlclient   2.2.8
python-socketio 5.16.1
```

### 3. Test Application Import
```bash
python -c "from app import app; print('✅ App loaded successfully')"
```

---

## 🎯 What You'll See

### When Server Starts:
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.100:5000
Press CTRL+C to quit
```

### In Your Browser:
1. **Homepage** - Welcome page with features
2. **Register** - Create your account
3. **Login** - Access your dashboard
4. **Dashboard** - Your personalized overview
5. **Voice Rooms** - NEW! Live collaboration feature

---

## 🔧 Troubleshooting

### Problem: "Port 5000 already in use"

**Solution 1:** Kill the process using port 5000
```bash
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

**Solution 2:** Change the port in app.py (line 351)
```python
socketio.run(app, debug=True, host='0.0.0.0', port=8080)
```
Then access: `http://127.0.0.1:8080`

### Problem: "MySQL connection failed"

**Solution:**
1. Open XAMPP Control Panel
2. Start MySQL (click "Start" button)
3. Wait for green "Running" status
4. Run: `python test_connection.py`

### Problem: "Module not found"

**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: "Database not found"

**Solution:**
```bash
python fix_and_connect.py
```

---

## 📊 Server Output Explained

### Normal Output:
```
✅ * Running on http://127.0.0.1:5000
   Server is running successfully

✅ 127.0.0.1 - - [19/Feb/2026 10:30:00] "GET / HTTP/1.1" 200
   Someone accessed the homepage

✅ 127.0.0.1 - - [19/Feb/2026 10:30:05] "GET /dashboard HTTP/1.1" 200
   Someone accessed the dashboard
```

### Error Output:
```
❌ Address already in use
   Port 5000 is busy - see troubleshooting above

❌ (2003, "Can't connect to MySQL server")
   MySQL is not running - start XAMPP MySQL

❌ ModuleNotFoundError: No module named 'flask_socketio'
   Dependencies missing - run: pip install -r requirements.txt
```

---

## 🎓 First Time Setup Checklist

Before running for the first time:

- [ ] MySQL/XAMPP installed and running
- [ ] Database created (run `python fix_and_connect.py`)
- [ ] Dependencies installed (run `pip install -r requirements.txt`)
- [ ] Voice rooms setup (run `python setup_voice_rooms.py`)
- [ ] Port 5000 available

---

## 🌐 URLs to Access

### Main Application
```
http://127.0.0.1:5000          - Homepage
http://127.0.0.1:5000/register - Register
http://127.0.0.1:5000/login    - Login
http://127.0.0.1:5000/dashboard - Dashboard
http://127.0.0.1:5000/voice-rooms - Voice Rooms (NEW!)
```

### Demo Mode (No Database Needed)
```
http://127.0.0.1:5000/demo     - Try without database
```

### Database Management
```
http://localhost/phpmyadmin    - phpMyAdmin
```

---

## 🛑 How to Stop the Server

### Method 1: In Terminal
Press `Ctrl + C`

### Method 2: Close Terminal Window
Just close the command prompt/PowerShell window

### Method 3: Task Manager
1. Open Task Manager (Ctrl + Shift + Esc)
2. Find "Python" process
3. Right-click → End Task

---

## 📱 Features Available

### Core Features
- ✅ User Registration & Login
- ✅ Find Study Partners
- ✅ Create & Join Study Groups
- ✅ Group Chat
- ✅ Notes Sharing (Upload/Download)
- ✅ Profile Management

### NEW: Voice Rooms 🎙️
- ✅ Live Video Calls (up to 6 on stage)
- ✅ Shared Whiteboard
- ✅ Real-time Chat
- ✅ Screen Sharing
- ✅ Unlimited Audience
- ✅ Stage Management

---

## 💡 Pro Tips

### Tip 1: Keep Terminal Open
Don't close the terminal window while using the app - it's running the server!

### Tip 2: Auto-Reload
The server auto-reloads when you change code (debug mode is on)

### Tip 3: Check Logs
Watch the terminal for errors and access logs

### Tip 4: Multiple Browsers
Test with different browsers or incognito mode for multiple users

### Tip 5: Network Access
Share your IP with friends on same WiFi to let them access

---

## 🎯 Quick Commands Reference

| Task | Command |
|------|---------|
| Run Project | `python app.py` |
| Test Database | `python test_connection.py` |
| Setup Database | `python fix_and_connect.py` |
| Setup Voice Rooms | `python setup_voice_rooms.py` |
| Install Dependencies | `pip install -r requirements.txt` |
| Check Dependencies | `pip list` |
| Find IP Address | `ipconfig` |

---

## 📞 Need Help?

### Check These First:
1. Is MySQL running? (XAMPP Control Panel)
2. Is port 5000 free? (Close other apps)
3. Are dependencies installed? (pip list)
4. Is database created? (python test_connection.py)

### Still Having Issues?
1. Read error message in terminal
2. Check troubleshooting section above
3. Review DEPLOYMENT_GUIDE.md
4. Check VOICE_ROOMS_GUIDE.md for voice rooms issues

---

## 🎉 Success Indicators

You'll know it's working when:

✅ Terminal shows "Running on http://127.0.0.1:5000"  
✅ Browser loads the homepage  
✅ You can register/login  
✅ Dashboard displays correctly  
✅ Voice Rooms menu appears  
✅ No error messages in terminal  

---

## 🚀 Ready to Start?

### Quick Start Command:
```bash
python app.py
```

### Or Double-Click:
```
RUN_PROJECT.bat
```

### Then Open Browser:
```
http://127.0.0.1:5000
```

---

**Happy Coding! 🎓✨**

*Your LearnLoop platform is ready to help students collaborate and learn together!*

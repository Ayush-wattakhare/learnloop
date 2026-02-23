# ⚡ LearnLoop - Quick Setup Guide

## 🎯 Goal: Get LearnLoop Running in 5 Minutes

---

## Option 1: With Database (Full Features) ✅

### Step 1: Start MySQL
```
Open XAMPP Control Panel → Start MySQL
```

### Step 2: Setup Database
```bash
python setup_database.py
```

### Step 3: Start Application
```bash
python app.py
```

### Step 4: Access
```
http://127.0.0.1:5000
```

---

## Option 2: Demo Mode (No Database) 🎭

### Step 1: Start Application
```bash
python app.py
```

### Step 2: Access Demo
```
http://127.0.0.1:5000/demo
```

**Demo Mode Features:**
- ✅ Browse all pages
- ✅ See sample data
- ✅ Test UI/UX
- ❌ Can't save data
- ❌ Can't create groups
- ❌ Can't upload files

---

## 🔧 One-Command Launcher

```bash
python start_project.py
```

This will:
- ✅ Check all dependencies
- ✅ Verify MySQL connection
- ✅ Create uploads folder
- ✅ Start the application
- ✅ Guide you if issues found

---

## 📋 Troubleshooting

### MySQL Not Running?
```
1. Open XAMPP Control Panel
2. Click "Start" next to MySQL
3. Wait for green status
4. Run: python test_connection.py
```

### Database Not Created?
```bash
python setup_database.py
```

### Dependencies Missing?
```bash
pip install -r requirements.txt
```

### Port 5000 Busy?
Edit `app.py` line 348:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

---

## 🎓 First Time User Journey

### 1. Register Account
```
http://127.0.0.1:5000/register
```

### 2. Login
```
http://127.0.0.1:5000/login
```

### 3. Explore Dashboard
- View your stats
- See suggested partners
- Browse groups

### 4. Find Study Partners
- Filter by semester
- Filter by college
- Connect with students

### 5. Create/Join Groups
- Create study group
- Join existing groups
- Start collaborating

### 6. Share & Chat
- Upload notes
- Send messages
- Download materials

---

## 🚀 Production Deployment

See `DEPLOYMENT_GUIDE.md` for:
- Security hardening
- Performance optimization
- Cloud deployment
- SSL configuration
- Monitoring setup

---

## 📞 Quick Commands

| Task | Command |
|------|---------|
| Setup Database | `python setup_database.py` |
| Test Connection | `python test_connection.py` |
| Start App | `python app.py` |
| Start with Checks | `python start_project.py` |
| Demo Mode | Visit `/demo` after starting |

---

## 🎯 Success Indicators

✅ MySQL running in XAMPP
✅ Database `learnloop` exists
✅ 5 tables created
✅ Flask server running on port 5000
✅ Can access homepage
✅ Can register/login

---

**Need help? Check `DEPLOYMENT_GUIDE.md` for detailed instructions!**

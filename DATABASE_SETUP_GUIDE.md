# 🗄️ Database Setup Guide - Fix MySQL Error

## ❌ Error You're Seeing

```
MySQLdb.OperationalError: (1045, "Access denied for user 'root'@'localhost' (using password: NO)")
```

This means MySQL database is not set up yet.

---

## ✅ GOOD NEWS!

Your app now works in **Demo Mode** without database! 

### Try Demo Mode Now:
```
http://localhost:5000/demo
```

Or click "Try Demo Mode" on the homepage!

---

## 🔧 To Enable Full Features (Setup Database)

### Option 1: Use XAMPP (Recommended for Windows)

#### Step 1: Install XAMPP
1. Download from: https://www.apachefriends.org/
2. Install (default settings are fine)
3. Run XAMPP Control Panel

#### Step 2: Start MySQL
1. Open XAMPP Control Panel
2. Click "Start" next to MySQL
3. Wait for green "Running" status

#### Step 3: Create Database
1. Click "Admin" next to MySQL (opens phpMyAdmin)
2. Or go to: http://localhost/phpmyadmin
3. Click "New" in left sidebar
4. Database name: `learnloop`
5. Click "Create"

#### Step 4: Import Schema
1. Click on `learnloop` database
2. Click "SQL" tab at top
3. Open `database.sql` file in text editor
4. Copy ALL the SQL code
5. Paste into SQL tab
6. Click "Go" button

#### Step 5: Restart Flask
```bash
# Stop current server (Ctrl+C)
# Start again
python app.py
```

#### Step 6: Test
```
http://localhost:5000
# Should now show "Get Started Free" button
```

---

### Option 2: Use MySQL Directly (Advanced)

#### If you have MySQL installed:

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE learnloop;

# Use database
USE learnloop;

# Import schema
SOURCE database.sql;

# Exit
EXIT;
```

---

### Option 3: Set MySQL Password (If you have password)

If your MySQL has a password, update `app.py`:

```python
# Find this line in app.py:
app.config['MYSQL_PASSWORD'] = ''

# Change to your password:
app.config['MYSQL_PASSWORD'] = 'your_password_here'
```

---

## 🎭 Using Demo Mode (No Database Needed)

### What Works in Demo Mode:
- ✅ Browse dashboard
- ✅ View study groups (4 demo groups)
- ✅ Find partners (6 demo students)
- ✅ View group details
- ✅ See chat messages
- ✅ Test all UI features

### What Doesn't Work:
- ❌ Create real accounts
- ❌ Create new groups
- ❌ Upload files
- ❌ Send messages
- ❌ Save data

### How to Access Demo:
```
http://localhost:5000/demo
```

Or click "Try Demo Mode" on homepage!

---

## 🔍 Troubleshooting

### Issue: XAMPP MySQL won't start

**Solution 1: Port 3306 in use**
```bash
# Check what's using port 3306
netstat -ano | findstr :3306

# Stop the process or change MySQL port in XAMPP
```

**Solution 2: Service conflict**
- Open Services (Win+R → services.msc)
- Stop "MySQL" service if running
- Try starting XAMPP MySQL again

### Issue: Can't access phpMyAdmin

**Solution:**
- Make sure Apache is also running in XAMPP
- Go to: http://localhost/phpmyadmin
- If still not working, restart XAMPP

### Issue: Database import fails

**Solution:**
- Make sure you selected the `learnloop` database first
- Copy SQL code in smaller chunks
- Check for error messages in phpMyAdmin

### Issue: Still getting MySQL error after setup

**Solution:**
```bash
# Restart Flask server
# Press Ctrl+C to stop
# Run again:
python app.py

# Check console for:
# "✅ MySQL connected" or
# "⚠️ MySQL not configured"
```

---

## 📊 Quick Status Check

### Check if MySQL is Running:
```bash
# Windows
netstat -ano | findstr :3306

# If you see output, MySQL is running
```

### Check if Database Exists:
```bash
# In phpMyAdmin or MySQL:
SHOW DATABASES;

# Should see 'learnloop' in the list
```

### Check if Tables Exist:
```bash
# In phpMyAdmin:
USE learnloop;
SHOW TABLES;

# Should see 5 tables:
# - users
# - groups
# - group_members
# - notes
# - messages
```

---

## 🎯 Recommended Approach

### For Quick Testing:
1. ✅ Use Demo Mode (no setup needed)
2. ✅ Test all features
3. ✅ Show to friends
4. ✅ Get feedback

### For Full Features:
1. ⏳ Install XAMPP (10 minutes)
2. ⏳ Setup database (5 minutes)
3. ⏳ Import schema (2 minutes)
4. ⏳ Restart Flask (1 minute)
5. ✅ Full features unlocked!

---

## 💡 Pro Tips

### Tip 1: Start with Demo
- Try demo mode first
- Understand features
- Then setup database

### Tip 2: XAMPP is Easiest
- All-in-one package
- Easy to use
- Perfect for development

### Tip 3: Keep XAMPP Running
- Start XAMPP when you work
- MySQL must be running
- Green status = good

### Tip 4: Backup Database
```bash
# In phpMyAdmin:
# Export → Go
# Saves your data
```

---

## 🆘 Still Having Issues?

### Check These:
1. ✅ XAMPP installed?
2. ✅ MySQL running (green in XAMPP)?
3. ✅ Database `learnloop` created?
4. ✅ Tables imported from database.sql?
5. ✅ Flask server restarted?

### Get Help:
- Check XAMPP logs
- Check Flask console output
- Try demo mode first
- Read error messages carefully

---

## ✅ Success Indicators

### You'll Know It Works When:
1. ✅ XAMPP shows MySQL running (green)
2. ✅ phpMyAdmin opens successfully
3. ✅ Database `learnloop` exists
4. ✅ 5 tables visible in database
5. ✅ Flask starts without MySQL error
6. ✅ Homepage shows "Get Started Free"
7. ✅ Can register new account
8. ✅ Can login successfully

---

## 🎉 Summary

### Without Database:
- Use Demo Mode
- Test all features
- Share with friends
- No setup needed

### With Database:
- Full features
- Create accounts
- Save data
- Upload files
- Send messages

**Both options work great! Choose what fits your needs! 🚀**

---

*Last Updated: February 19, 2026*  
*Status: Demo Mode Active, Database Optional*

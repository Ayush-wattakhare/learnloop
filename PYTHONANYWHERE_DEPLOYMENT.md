# 🚀 Deploy LearnLoop to PythonAnywhere

## Step-by-Step Deployment Guide

---

## 📋 Prerequisites

- ✅ LearnLoop rebranded and tested locally
- ✅ PythonAnywhere account (free)
- ✅ All files ready for upload

---

## 🎯 Step 1: Create PythonAnywhere Account

1. Go to: **https://www.pythonanywhere.com**
2. Click **"Start running Python online in less than a minute!"**
3. Choose **"Create a Beginner account"** (FREE)
4. Fill in:
   - Username (e.g., `learnloop` or your name)
   - Email
   - Password
5. Verify email
6. Login to dashboard

---

## 📁 Step 2: Upload Your Code

### Option A: Upload via Web Interface

1. Click **"Files"** tab in dashboard
2. Navigate to: `/home/yourusername/`
3. Click **"Upload a file"**
4. Upload these files one by one:
   - `app.py`
   - `voice_room_routes.py`
   - `requirements.txt`
   - `setup_learnloop_database.py`

5. Create folders and upload:
   - Create `templates/` folder → Upload all HTML files
   - Create `static/` folder → Upload CSS, JS, images
   - Create `static/uploads/` folder
   - Create `static/uploads/profiles/` folder
   - Create `static/uploads/messages/` folder
   - Create `static/uploads/notes/` folder

### Option B: Upload via Git (Recommended)

1. Click **"Consoles"** tab
2. Start a **"Bash"** console
3. Run:
```bash
cd ~
git clone https://github.com/yourusername/learnloop.git
# Or upload as zip and extract
```

---

## 🗄️ Step 3: Setup MySQL Database

1. Click **"Databases"** tab
2. Click **"Initialize MySQL"**
3. Set a password (remember this!)
4. Wait for initialization (takes 1-2 minutes)

5. Create database:
   - In "Create database" section
   - Database name: `yourusername$learnloop`
   - Click **"Create"**

6. Setup tables:
   - Go to **"Consoles"** tab
   - Start **"Bash"** console
   - Run:
```bash
cd ~/learnloop
python3 setup_learnloop_database.py
```

**Note:** Update `setup_learnloop_database.py` with PythonAnywhere credentials:
```python
db = MySQLdb.connect(
    host="yourusername.mysql.pythonanywhere-services.com",
    user="yourusername",
    passwd="your-mysql-password",
    db="yourusername$learnloop"
)
```

---

## 🐍 Step 4: Setup Virtual Environment

1. Go to **"Consoles"** tab
2. Start **"Bash"** console
3. Run:

```bash
# Create virtual environment
mkvirtualenv learnloop --python=python3.10

# Activate it (should auto-activate)
workon learnloop

# Navigate to project
cd ~/learnloop

# Install dependencies
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask-2.3.0 Flask-MySQLdb-1.0.1 ...
```

---

## 🌐 Step 5: Create Web App

1. Click **"Web"** tab
2. Click **"Add a new web app"**
3. Choose your domain: `yourusername.pythonanywhere.com`
4. Click **"Next"**
5. Select **"Manual configuration"**
6. Choose **"Python 3.10"**
7. Click **"Next"**

---

## ⚙️ Step 6: Configure Web App

### A. Set Virtual Environment

1. In **"Web"** tab, scroll to **"Virtualenv"** section
2. Enter: `/home/yourusername/.virtualenvs/learnloop`
3. Click checkmark to save

### B. Configure WSGI File

1. In **"Web"** tab, find **"Code"** section
2. Click on **"WSGI configuration file"** link
3. **Delete all content** and replace with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/learnloop'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['MYSQL_HOST'] = 'yourusername.mysql.pythonanywhere-services.com'
os.environ['MYSQL_USER'] = 'yourusername'
os.environ['MYSQL_PASSWORD'] = 'your-mysql-password'
os.environ['MYSQL_DB'] = 'yourusername$learnloop'
os.environ['PRODUCTION'] = 'True'

# Import Flask app
from app import app as application
```

4. Click **"Save"** (top right)

### C. Set Static Files

1. In **"Web"** tab, scroll to **"Static files"** section
2. Add mapping:
   - URL: `/static/`
   - Directory: `/home/yourusername/learnloop/static/`
3. Click checkmark to save

---

## 🔧 Step 7: Update app.py for Production

Edit `app.py` to use environment variables:

```python
import os

# Database Config - Use environment variables in production
if os.environ.get('PRODUCTION'):
    app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
    app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
    app.secret_key = os.environ.get('SECRET_KEY', 'learnloop_secret_2024')
    app.config['DEBUG'] = False
else:
    # Local development
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'learnloop'
    app.secret_key = 'learnloop_secret_2024'
    app.config['DEBUG'] = True
```

Upload the updated `app.py` file.

---

## 🚀 Step 8: Launch Your App

1. Go to **"Web"** tab
2. Click the big green **"Reload"** button
3. Wait for reload to complete (10-30 seconds)
4. Click on your URL: `yourusername.pythonanywhere.com`

**🎉 Your app should now be live!**

---

## ✅ Step 9: Test Your Deployment

Visit: `https://yourusername.pythonanywhere.com`

Test these features:
- [ ] Homepage loads
- [ ] Register new account
- [ ] Login works
- [ ] Dashboard displays
- [ ] Profile picture upload
- [ ] Find partners
- [ ] Create group
- [ ] Send messages
- [ ] Create voice room

---

## 🐛 Troubleshooting

### Error: "Something went wrong"

1. Check **"Web"** tab → **"Log files"** section
2. Click **"Error log"** to see errors
3. Common issues:

**Import Error:**
```
ModuleNotFoundError: No module named 'flask'
```
**Solution:**
```bash
workon learnloop
pip install -r requirements.txt
```

**Database Connection Error:**
```
Can't connect to MySQL server
```
**Solution:**
- Check WSGI file has correct credentials
- Verify database name: `yourusername$learnloop`
- Check MySQL is initialized

**Static Files Not Loading:**
```
404 on /static/css/style.css
```
**Solution:**
- Check static files mapping in Web tab
- Verify path: `/home/yourusername/learnloop/static/`

### Socket.IO Not Working

PythonAnywhere free tier doesn't support WebSockets. To fix:

1. Edit `app.py`:
```python
# For PythonAnywhere, use polling instead of websockets
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
```

2. Or disable Socket.IO features temporarily

---

## 📊 Monitor Your App

### View Logs

1. **"Web"** tab → **"Log files"**
2. **Error log**: Shows Python errors
3. **Server log**: Shows requests
4. **Access log**: Shows all visits

### Check Database

1. **"Databases"** tab
2. Click **"Go to console"** next to your database
3. Run SQL queries:
```sql
SELECT COUNT(*) FROM users;
SELECT * FROM groups;
```

---

## 🔒 Security for Production

### 1. Change Secret Key

Generate new secret key:
```python
import secrets
print(secrets.token_hex(32))
```

Update in WSGI file:
```python
os.environ['SECRET_KEY'] = 'your-new-secret-key-here'
```

### 2. Disable Debug Mode

In `app.py`:
```python
app.config['DEBUG'] = False
```

### 3. Set Strong MySQL Password

In **"Databases"** tab, you can change MySQL password.

---

## 📈 Upgrade Options

### Free Tier Limits:
- ✅ 512 MB disk space
- ✅ 1 web app
- ✅ MySQL database
- ❌ No WebSockets
- ❌ Limited CPU time

### Paid Tiers ($5/month):
- ✅ More disk space
- ✅ Multiple web apps
- ✅ WebSocket support
- ✅ More CPU time
- ✅ Custom domains

---

## 🌐 Custom Domain (Optional)

### With Paid Account:

1. Buy domain (Namecheap, GoDaddy, etc.)
2. In **"Web"** tab, add domain
3. Update DNS records:
   - CNAME: `www` → `yourusername.pythonanywhere.com`
4. Wait for DNS propagation (24-48 hours)

---

## 🔄 Update Your App

### When you make changes:

1. Upload new files via **"Files"** tab
2. Or use Git:
```bash
cd ~/learnloop
git pull origin main
```

3. Reload web app:
   - Go to **"Web"** tab
   - Click **"Reload"** button

---

## 📱 Share Your App

### Your Public URL:
```
https://yourusername.pythonanywhere.com
```

### Share with:
- Friends and classmates
- Social media
- Email
- QR code (generate online)

### Promote:
- "Check out LearnLoop - Study collaboration platform!"
- "Join me on LearnLoop: [your-url]"
- "Free study groups and voice rooms!"

---

## 💾 Backup Your Data

### Export Database:

1. **"Databases"** tab
2. Click **"Go to console"**
3. Run:
```bash
mysqldump -u yourusername -h yourusername.mysql.pythonanywhere-services.com -p 'yourusername$learnloop' > backup.sql
```

### Download Files:

1. **"Files"** tab
2. Navigate to folders
3. Download important files

---

## 📞 Get Help

### PythonAnywhere Support:
- Help pages: https://help.pythonanywhere.com/
- Forums: https://www.pythonanywhere.com/forums/
- Email: support@pythonanywhere.com

### Common Resources:
- Flask deployment: https://help.pythonanywhere.com/pages/Flask/
- MySQL setup: https://help.pythonanywhere.com/pages/MySQL/
- File uploads: https://help.pythonanywhere.com/pages/UploadingAndDownloadingFiles/

---

## ✅ Deployment Checklist

- [ ] PythonAnywhere account created
- [ ] Files uploaded
- [ ] MySQL database initialized
- [ ] Database tables created
- [ ] Virtual environment setup
- [ ] Dependencies installed
- [ ] Web app created
- [ ] WSGI file configured
- [ ] Static files mapped
- [ ] App reloaded
- [ ] Site accessible
- [ ] All features tested
- [ ] Logs checked
- [ ] URL shared

---

## 🎉 Congratulations!

**LearnLoop is now live on the internet!**

Your app is accessible at:
```
https://yourusername.pythonanywhere.com
```

Anyone in the world can now:
- Register and create accounts
- Find study partners
- Create study groups
- Use voice rooms
- Share files and collaborate

**Start sharing your URL and building your community!** 🚀

---

*Deployment Guide for LearnLoop*
*Platform: PythonAnywhere (Free Tier)*
*Status: READY TO DEPLOY ✅*

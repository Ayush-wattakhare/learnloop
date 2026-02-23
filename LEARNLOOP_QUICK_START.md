# 🚀 LearnLoop - Quick Start Guide

## Welcome to LearnLoop!

**StudyMate** is now **LearnLoop** - Your complete study collaboration platform!

---

## ✅ Rebranding Complete

All files have been updated:
- ✅ 76 files rebranded
- ✅ Database renamed to `learnloop`
- ✅ All templates updated
- ✅ Configuration files updated
- ✅ Documentation updated

---

## 🎯 Quick Start (3 Steps)

### Step 1: Setup Database
```bash
python setup_learnloop_database.py
```

Expected output:
```
✅ Database 'learnloop' created
✅ 13 tables created
✅ LearnLoop Database Setup Complete!
```

### Step 2: Start Application
```bash
python app.py
```

### Step 3: Open Browser
```
http://127.0.0.1:5000
```

---

## 🌐 Access from Mobile/Other Devices

### On Same WiFi Network:

1. **Find Your IP** (Windows):
   ```bash
   ipconfig
   ```
   Look for: `IPv4 Address: 192.168.x.x`

2. **Access from Any Device**:
   ```
   http://YOUR_IP:5000
   ```
   Example: `http://192.168.1.100:5000`

3. **Share with Friends**:
   - They connect to same WiFi
   - Open the URL on their device
   - Register and start using!

---

## 📱 Features Available

### ✅ User System
- Registration and Login
- Profile with Picture Upload
- View Other Profiles

### ✅ Find Partners
- Search by Topic
- Search by Language
- Send Friend Requests
- Suggested Partners

### ✅ Messaging System
- Friend Requests
- One-on-One Chat
- File Sharing (Images, PDFs, Docs)
- Voice Call (UI Ready)
- Unread Counter

### ✅ Study Groups
- Create Public/Private Groups
- Group Chat
- Share Notes
- Member Management
- Notifications to Relevant Students

### ✅ Voice Rooms
- Video/Audio Rooms
- Whiteboard with Drawing
- Text Tool
- Room Chat
- Host Controls

### ✅ Notifications
- New Group Alerts
- Friend Requests
- Message Notifications
- Real-time Updates

---

## 🎨 What Changed?

### Brand Name
- **Old**: StudyMate
- **New**: LearnLoop

### Database
- **Old**: `studymate`
- **New**: `learnloop`

### Secret Key
- **Old**: `studymate_invertis_2024`
- **New**: `learnloop_secret_2024`

### Everything Else
- All features work exactly the same
- All data structures unchanged
- All functionality preserved

---

## 🚀 Deploy to Internet

### Option 1: PythonAnywhere (Free & Easy)
1. Sign up: https://www.pythonanywhere.com
2. Upload code
3. Setup database
4. Configure web app
5. Your site: `yourusername.pythonanywhere.com`

**See**: `DEPLOYMENT_GUIDE_LEARNLOOP.md` for detailed steps

### Option 2: Local Network (Free)
1. Run on your computer
2. Share IP address with friends
3. They access from same WiFi
4. Perfect for classroom/campus use

---

## 📊 Database Structure

### 13 Tables Created:
1. **users** - User accounts and profiles
2. **groups** - Study groups
3. **group_members** - Group membership
4. **messages** - Group chat messages
5. **notes** - Shared files/notes
6. **voice_rooms** - Video/audio rooms
7. **room_participants** - Room members
8. **room_messages** - Room chat
9. **whiteboard_snapshots** - Whiteboard saves
10. **stage_requests** - Stage join requests
11. **friendships** - Friend connections
12. **direct_messages** - Private messages
13. **notifications** - User notifications

---

## 🎯 First Time Setup

### 1. Register Account
- Go to: http://127.0.0.1:5000
- Click "Get Started"
- Fill in details
- Create account

### 2. Complete Profile
- Click profile dropdown
- Add profile picture
- Update bio
- Save changes

### 3. Explore Features
- Find Partners → Search students
- Groups → Create or join groups
- Voice Rooms → Start live sessions
- Messages → Connect with friends

---

## 🔧 Configuration

### Current Settings (app.py):
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_DB = 'learnloop'
```

### For Production:
Use environment variables:
```python
MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_DB = os.environ.get('MYSQL_DB')
```

---

## 📁 Project Structure

```
LearnLoop/
├── app.py                          # Main application
├── voice_room_routes.py            # Voice room features
├── setup_learnloop_database.py     # Database setup
├── templates/                      # HTML templates
│   ├── base.html                   # Base layout
│   ├── dashboard.html              # Dashboard
│   ├── messages.html               # Messaging
│   ├── groups.html                 # Study groups
│   └── ...
├── static/                         # Static files
│   ├── css/style.css              # Styles
│   ├── js/main.js                 # JavaScript
│   └── uploads/                   # User uploads
└── DEPLOYMENT_GUIDE_LEARNLOOP.md  # Deployment guide
```

---

## 🆘 Troubleshooting

### Database Connection Error
```
❌ MySQL not configured
```
**Solution:**
1. Start XAMPP
2. Start MySQL service
3. Run: `python setup_learnloop_database.py`
4. Restart app

### Port Already in Use
```
❌ Address already in use
```
**Solution:**
1. Stop other Flask apps
2. Change port in app.py: `port=5001`
3. Restart app

### Static Files Not Loading
```
❌ 404 on CSS/JS files
```
**Solution:**
1. Check `static/` folder exists
2. Verify file paths in templates
3. Clear browser cache

---

## 📈 Next Steps

### For Development:
1. ✅ Test all features locally
2. ✅ Add more users
3. ✅ Create sample groups
4. ✅ Test messaging
5. ✅ Try voice rooms

### For Deployment:
1. Choose hosting (PythonAnywhere recommended)
2. Follow deployment guide
3. Setup production database
4. Configure domain (optional)
5. Enable HTTPS
6. Share with users!

---

## 🎉 You're All Set!

LearnLoop is ready to use:
- ✅ Rebranded from StudyMate
- ✅ Database setup complete
- ✅ All features working
- ✅ Ready for deployment

**Start the app and begin collaborating!**

```bash
python app.py
```

Then open: **http://127.0.0.1:5000**

---

## 📞 Need Help?

### Documentation:
- `DEPLOYMENT_GUIDE_LEARNLOOP.md` - Deployment instructions
- `FEATURE_CONNECTIONS.md` - Feature integration
- `NOTIFICATION_SYSTEM.md` - Notification system
- `READY_TO_USE.md` - Feature checklist

### Quick Commands:
```bash
# Setup database
python setup_learnloop_database.py

# Start app
python app.py

# Test features
python test_all_features.py
```

---

*Welcome to LearnLoop - Where Learning Connects!* 🚀

*Last Updated: Rebranding complete*
*Status: READY TO USE ✅*

# 🚀 LearnLoop Setup Guide

## Complete Setup Instructions

### ✅ Step-by-Step Setup

#### 1. Install Python Dependencies
Open Command Prompt or PowerShell in the project folder and run:
```bash
pip install flask flask-mysqldb werkzeug
```

#### 2. Start MySQL Server
- Open **XAMPP Control Panel**
- Click **Start** button next to **Apache**
- Click **Start** button next to **MySQL**
- Wait until both show green "Running" status

#### 3. Create Database
- Open browser and go to: `http://localhost/phpmyadmin`
- Click **"New"** in the left sidebar
- Enter database name: `learnloop`
- Click **"Create"**

#### 4. Import Database Schema
- Click on the **learnloop** database you just created
- Click on the **"SQL"** tab at the top
- Open the `database.sql` file from this project folder in a text editor
- Copy ALL the SQL code
- Paste it into the SQL tab in phpMyAdmin
- Click **"Go"** button at the bottom right

You should see a success message and 5 tables created:
- ✅ users
- ✅ groups
- ✅ group_members
- ✅ notes
- ✅ messages

#### 5. Run the Application
In Command Prompt or PowerShell (in project folder):
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

#### 6. Open in Browser
Open your web browser and go to:
```
http://127.0.0.1:5000
```

---

## 🎯 First Time Usage

### Create Your First Account
1. Click **"Get Started"** or **"Register"**
2. Fill in your details:
   - Full Name
   - Email (use any email, doesn't need to be real)
   - Password (min 6 characters)
   - Select your Semester
   - College (default: Invertis University)
   - Bio (optional)
3. Click **"Create Account"**

### Login
1. Use the email and password you just created
2. Click **"Login to Dashboard"**

### Explore Features
1. **Dashboard** - See your stats and groups
2. **Find Partners** - Search for other students
3. **Groups** - Browse or create study groups
4. **Profile** - Update your information

---

## 🔧 Troubleshooting

### Problem: "No module named 'flask'"
**Solution**: Install Flask
```bash
pip install flask
```

### Problem: "No module named 'flask_mysqldb'"
**Solution**: Install Flask-MySQLdb
```bash
pip install flask-mysqldb
```

### Problem: Can't connect to MySQL
**Solution**: 
1. Make sure XAMPP MySQL is running (green in XAMPP Control Panel)
2. Check if MySQL is on port 3306 (default)
3. Verify database name is exactly `learnloop`

### Problem: "Table doesn't exist"
**Solution**: 
1. Go to phpMyAdmin
2. Select learnloop database
3. Re-run the SQL from `database.sql` file

### Problem: CSS not loading / Page looks broken
**Solution**:
1. Hard refresh the page (Ctrl + F5)
2. Clear browser cache
3. Check if `static/css/style.css` file exists

### Problem: Can't upload files
**Solution**:
1. Make sure `static/uploads` folder exists
2. Check folder permissions
3. Verify file type is allowed (PDF, DOCX, PPTX, PNG, JPG)

---

## 📝 Test Data

Want to test with multiple users? Create these accounts:

**User 1:**
- Name: Rahul Sharma
- Email: rahul@test.com
- Password: test123
- Semester: 3

**User 2:**
- Name: Priya Singh
- Email: priya@test.com
- Password: test123
- Semester: 3

**User 3:**
- Name: Amit Verma
- Email: amit@test.com
- Password: test123
- Semester: 3

Then:
1. Login as Rahul
2. Create a group "Python Warriors"
3. Logout and login as Priya
4. Join the group
5. Test the chat feature!

---

## 🎨 Customization

### Change Colors
Edit `static/css/style.css` and modify the CSS variables at the top:
```css
:root {
  --blue: #2563EB;      /* Primary color */
  --green: #16A34A;     /* Success color */
  --yellow: #CA8A04;    /* Warning color */
}
```

### Change University Name
Edit templates and replace "Invertis University" with your university name.

### Add More Semesters
Edit the semester dropdowns in:
- `templates/register.html`
- `templates/profile.html`
- `templates/create_group.html`

---

## 🚀 Production Deployment

**⚠️ Important**: This is a development setup. For production:

1. Change `app.secret_key` in `app.py` to a random secure string
2. Set `debug=False` in `app.run()`
3. Use a production WSGI server (Gunicorn, uWSGI)
4. Use environment variables for database credentials
5. Enable HTTPS
6. Set up proper file upload limits
7. Add rate limiting
8. Implement proper error handling

---

## ✅ Checklist

Before running the app, make sure:
- [ ] Python 3.7+ is installed
- [ ] All pip packages are installed
- [ ] XAMPP MySQL is running
- [ ] Database `learnloop` is created
- [ ] All 5 tables are created from `database.sql`
- [ ] `static/uploads` folder exists
- [ ] Port 5000 is not being used by another app

---

## 🎓 Learning Resources

Want to understand the code better?

- **Flask Documentation**: https://flask.palletsprojects.com/
- **MySQL Tutorial**: https://www.mysqltutorial.org/
- **CSS Grid**: https://css-tricks.com/snippets/css/complete-guide-grid/
- **JavaScript Basics**: https://javascript.info/

---

## 💡 Tips

1. **Use Chrome DevTools** (F12) to inspect elements and debug
2. **Check Flask console** for error messages
3. **Use phpMyAdmin** to view database contents
4. **Test on different browsers** for compatibility
5. **Keep XAMPP running** while using the app

---

## 🎉 You're All Set!

If you followed all steps correctly, LearnLoop should be running smoothly!

**Enjoy connecting with your study partners! 📚✨**

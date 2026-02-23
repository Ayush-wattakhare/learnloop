# 🚀 LearnLoop Deployment Guide

## Overview
Complete guide to deploy LearnLoop on a server for public access.

---

## ✅ Rebranding Complete!

**StudyMate** has been successfully rebranded to **LearnLoop**

- ✅ 76 files updated
- ✅ All templates rebranded
- ✅ Database schema updated
- ✅ Configuration files updated

---

## 📋 Pre-Deployment Checklist

### Local Setup Complete
- ✅ Database: `learnloop` created
- ✅ All 13 tables created
- ✅ Application rebranded
- ✅ Features tested locally

### Ready for Deployment
- ✅ Python Flask application
- ✅ MySQL database
- ✅ Static files (CSS, JS, images)
- ✅ File upload directories

---

## 🌐 Deployment Options

### Option 1: PythonAnywhere (Recommended - Free)

**Why PythonAnywhere?**
- ✅ Free tier available
- ✅ Python/Flask support built-in
- ✅ MySQL database included
- ✅ Easy deployment
- ✅ HTTPS by default
- ✅ No credit card required

**Steps:**

1. **Sign Up**
   - Go to: https://www.pythonanywhere.com
   - Click "Start running Python online in less than a minute!"
   - Create free account

2. **Upload Code**
   - Go to "Files" tab
   - Upload your project files
   - Or use Git: `git clone your-repo-url`

3. **Setup Virtual Environment**
   ```bash
   mkvirtualenv learnloop --python=python3.10
   pip install flask flask-mysqldb flask-socketio werkzeug
   ```

4. **Setup Database**
   - Go to "Databases" tab
   - Initialize MySQL
   - Create database: `learnloop`
   - Run: `python setup_learnloop_database.py`

5. **Configure Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Flask"
   - Set source code path
   - Set WSGI configuration

6. **Update Configuration**
   Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`:
   ```python
   import sys
   path = '/home/yourusername/learnloop'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

7. **Set Environment Variables**
   In WSGI file:
   ```python
   import os
   os.environ['MYSQL_HOST'] = 'yourusername.mysql.pythonanywhere-services.com'
   os.environ['MYSQL_USER'] = 'yourusername'
   os.environ['MYSQL_PASSWORD'] = 'your-password'
   os.environ['MYSQL_DB'] = 'yourusername$learnloop'
   ```

8. **Reload Web App**
   - Click "Reload" button
   - Visit: `yourusername.pythonanywhere.com`

---

### Option 2: Heroku (Free Tier)

**Steps:**

1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App**
   ```bash
   heroku login
   heroku create learnloop-app
   ```

3. **Add MySQL Database**
   ```bash
   heroku addons:create cleardb:ignite
   ```

4. **Create Procfile**
   ```
   web: gunicorn app:app
   ```

5. **Create requirements.txt**
   ```
   Flask==2.3.0
   Flask-MySQLdb==1.0.1
   Flask-SocketIO==5.3.0
   gunicorn==21.2.0
   ```

6. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Deploy LearnLoop"
   git push heroku master
   ```

7. **Setup Database**
   ```bash
   heroku run python setup_learnloop_database.py
   ```

---

### Option 3: DigitalOcean/AWS/Azure

**Requirements:**
- VPS/Server with Ubuntu
- Root access
- Domain name (optional)

**Steps:**

1. **Setup Server**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip mysql-server nginx
   ```

2. **Install Dependencies**
   ```bash
   pip3 install flask flask-mysqldb flask-socketio gunicorn
   ```

3. **Setup MySQL**
   ```bash
   sudo mysql_secure_installation
   mysql -u root -p
   CREATE DATABASE learnloop;
   CREATE USER 'learnloop'@'localhost' IDENTIFIED BY 'password';
   GRANT ALL ON learnloop.* TO 'learnloop'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. **Upload Code**
   ```bash
   scp -r /path/to/learnloop user@server:/var/www/
   ```

5. **Configure Gunicorn**
   Create `/etc/systemd/system/learnloop.service`:
   ```ini
   [Unit]
   Description=LearnLoop Flask App
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/learnloop
   ExecStart=/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:8000 app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

6. **Configure Nginx**
   Create `/etc/nginx/sites-available/learnloop`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static {
           alias /var/www/learnloop/static;
       }
   }
   ```

7. **Enable and Start**
   ```bash
   sudo systemctl enable learnloop
   sudo systemctl start learnloop
   sudo systemctl enable nginx
   sudo systemctl restart nginx
   ```

---

## 🔧 Configuration for Production

### Update app.py

```python
import os

# Production configuration
if os.environ.get('PRODUCTION'):
    app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
    app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
    app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '')
    app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'learnloop')
    app.secret_key = os.environ.get('SECRET_KEY', 'learnloop_secret_2024')
else:
    # Development configuration
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'learnloop'
    app.secret_key = 'learnloop_secret_2024'
```

---

## 📱 Enable Mobile Access (Local Network)

### Current Setup
Your app runs on: `http://127.0.0.1:5000`

### Make Accessible on Network

1. **Find Your IP Address**
   ```bash
   # Windows
   ipconfig
   # Look for IPv4 Address (e.g., 192.168.1.100)
   ```

2. **Update app.py**
   ```python
   if __name__ == '__main__':
       socketio.run(app, debug=True, host='0.0.0.0', port=5000)
   ```

3. **Allow Firewall**
   - Windows: Allow Python through firewall
   - Settings → Firewall → Allow an app

4. **Access from Mobile**
   - Connect to same WiFi
   - Open: `http://YOUR_IP:5000`
   - Example: `http://192.168.1.100:5000`

---

## 🔒 Security Checklist

### Before Going Live

- [ ] Change secret key
- [ ] Use environment variables
- [ ] Enable HTTPS
- [ ] Set strong MySQL password
- [ ] Disable debug mode
- [ ] Add rate limiting
- [ ] Enable CORS properly
- [ ] Validate all inputs
- [ ] Add CSRF protection
- [ ] Regular backups

### Update Secret Key
```python
import secrets
print(secrets.token_hex(32))
# Use this as your secret key
```

---

## 📊 Database Migration

### Export from Local
```bash
mysqldump -u root -p learnloop > learnloop_backup.sql
```

### Import to Server
```bash
mysql -u username -p learnloop < learnloop_backup.sql
```

---

## 🎯 Post-Deployment

### Test Everything
- [ ] User registration
- [ ] Login/logout
- [ ] Profile upload
- [ ] Find partners
- [ ] Friend requests
- [ ] Messaging
- [ ] File sharing
- [ ] Study groups
- [ ] Voice rooms
- [ ] Notifications

### Monitor
- Check error logs
- Monitor database size
- Track user registrations
- Monitor server resources

---

## 🌐 Custom Domain (Optional)

### Steps:
1. Buy domain (Namecheap, GoDaddy, etc.)
2. Point DNS to server IP
3. Setup SSL certificate (Let's Encrypt)
4. Configure Nginx for domain

### Free SSL with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## 📈 Scaling Tips

### Performance
- Use Redis for sessions
- Enable caching
- Optimize database queries
- Use CDN for static files
- Enable gzip compression

### Database
- Add indexes
- Regular backups
- Monitor slow queries
- Use connection pooling

---

## 🆘 Troubleshooting

### Common Issues

**Database Connection Failed**
- Check MySQL is running
- Verify credentials
- Check firewall rules

**Static Files Not Loading**
- Check file permissions
- Verify static folder path
- Check Nginx configuration

**Socket.IO Not Working**
- Enable WebSocket in Nginx
- Check CORS settings
- Verify Socket.IO version

---

## 📞 Support

### Resources
- Flask Documentation: https://flask.palletsprojects.com/
- PythonAnywhere Help: https://help.pythonanywhere.com/
- MySQL Documentation: https://dev.mysql.com/doc/

---

## ✅ Deployment Checklist

- [ ] Code rebranded to LearnLoop
- [ ] Database created and migrated
- [ ] Server/hosting chosen
- [ ] Application deployed
- [ ] Database connected
- [ ] Static files serving
- [ ] File uploads working
- [ ] HTTPS enabled
- [ ] Domain configured (optional)
- [ ] Tested all features
- [ ] Monitoring setup
- [ ] Backups configured

---

## 🎉 You're Ready!

LearnLoop is now ready for deployment. Choose your hosting option and follow the steps above.

**Recommended for beginners:** Start with PythonAnywhere (free and easy)

**For production:** Use DigitalOcean/AWS with proper security

---

*Last Updated: LearnLoop rebranding complete*
*Status: READY FOR DEPLOYMENT ✅*

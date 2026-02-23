# LearnLoop 📚
### A Modern Study Group Finder for BCA Students — Invertis University

A beautifully designed web application that helps students connect with study partners, create study groups, share notes, and collaborate effectively.

---

## ✨ Features

### 🎯 Core Features
- **User Authentication** - Secure registration and login with password hashing
- **Find Study Partners** - Search and filter students by semester and college
- **Study Groups** - Create, join, and manage study groups
- **Group Chat** - Real-time messaging within study groups
- **Notes Sharing** - Upload and download study materials (PDF, DOCX, PPTX, images)
- **Dashboard** - Personalized overview with stats, groups, and recent activity
- **Profile Management** - Update your information and preferences

### 🎨 Design Features
- Modern gradient UI with smooth animations
- Responsive design that works on all devices
- Custom avatars with gradient backgrounds
- Interactive cards with hover effects
- Clean typography using Plus Jakarta Sans font
- Intuitive navigation and user experience

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.7 or higher
- MySQL (via XAMPP or standalone)
- Modern web browser

### Step 1 — Install Dependencies
```bash
pip install flask flask-mysqldb werkzeug
```

### Step 2 — Setup MySQL Database
1. **Start XAMPP**
   - Open XAMPP Control Panel
   - Click "Start" for Apache and MySQL
   - Wait for both to show green "Running" status

2. **Create Database**
   - Open browser: `http://localhost/phpmyadmin`
   - Click "New" in left sidebar
   - Database name: `learnloop`
   - Click "Create"

3. **Import Schema**
   - Click on `learnloop` database
   - Go to "SQL" tab
   - Open `database.sql` file from project folder
   - Copy all SQL code and paste into SQL tab
   - Click "Go" to execute

### Step 3 — Run the Application
```bash
python app.py
```

### Step 4 — Access the App
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
LearnLoop/
│
├── app.py                  # Main Flask application with all routes
├── database.sql            # MySQL database schema
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── static/                # Static assets
│   ├── css/
│   │   └── style.css      # Modern CSS with gradients and animations
│   ├── js/
│   │   └── main.js        # JavaScript for interactivity
│   └── uploads/           # User-uploaded files (notes, PDFs)
│
└── templates/             # HTML templates
    ├── base.html          # Base template with navbar
    ├── index.html         # Landing page with hero section
    ├── login.html         # Login page
    ├── register.html      # Registration page
    ├── dashboard.html     # User dashboard with stats
    ├── find_partners.html # Search study partners
    ├── groups.html        # Browse all groups
    ├── group.html         # Group detail with chat
    ├── create_group.html  # Create new group
    └── profile.html       # Edit user profile
```

---

## 🛠 Tech Stack

### Backend
- **Flask** - Python web framework
- **MySQL** - Database management
- **Flask-MySQLdb** - MySQL integration
- **Werkzeug** - Password hashing and security

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS variables
- **JavaScript** - Interactive features
- **Google Fonts** - Plus Jakarta Sans & Space Mono

### Design
- Custom CSS with CSS variables for theming
- Gradient backgrounds and modern color palette
- Responsive grid layouts
- Smooth animations and transitions
- Card-based UI components

---

## 📊 Database Schema

### Tables
1. **users** - Student profiles and authentication
2. **groups** - Study group information
3. **group_members** - Many-to-many relationship (users ↔ groups)
4. **notes** - Uploaded study materials
5. **messages** - Group chat messages

---

## 🎨 Design System

### Color Palette
- **Primary Blue**: `#2563EB`
- **Success Green**: `#16A34A`
- **Warning Yellow**: `#CA8A04`
- **Indigo**: `#4F46E5`
- **Purple**: `#7C3AED`

### Typography
- **Headings**: Plus Jakarta Sans (800 weight)
- **Body**: Plus Jakarta Sans (400-600 weight)
- **Monospace**: Space Mono (for branding)

### Components
- Modern cards with shadows
- Gradient avatars
- Colored badges
- Smooth hover effects
- Responsive grids

---

## 🔒 Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Login required decorators
- Secure file uploads with validation
- SQL injection prevention with parameterized queries

---

## 📱 Responsive Design

The application is fully responsive and works seamlessly on:
- Desktop computers (1920px+)
- Laptops (1366px - 1920px)
- Tablets (768px - 1366px)
- Mobile phones (320px - 768px)

---

## 🚧 Future Enhancements

- [ ] Real-time chat with WebSockets
- [ ] Email notifications
- [ ] File preview before download
- [ ] Advanced search filters
- [ ] Group admin controls
- [ ] Direct messaging between users
- [ ] Calendar integration for study sessions
- [ ] Mobile app (React Native)

---

## 👨‍💻 Developer

**BCA 2nd Year Student**  
Invertis University, Bareilly, UP

---

## 📄 License

This project is created for educational purposes as part of BCA curriculum at Invertis University.

---

## 🤝 Contributing

This is a student project. Suggestions and improvements are welcome!

---

## 📞 Support

For issues or questions:
1. Check the database connection in `app.py`
2. Ensure MySQL is running via XAMPP
3. Verify all dependencies are installed
4. Check browser console for JavaScript errors

---

## 🎓 About LearnLoop

LearnLoop was created to solve a real problem faced by BCA students at Invertis University - finding the right study partners and collaborating effectively. The platform makes it easy to:

- Connect with classmates in your semester
- Form focused study groups by subject
- Share notes and resources
- Communicate and plan study sessions
- Build a supportive learning community

**Happy Studying! 📚✨**

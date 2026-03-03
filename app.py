from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify, send_from_directory
try:
    from flask_mysqldb import MySQL
except ImportError:
    MySQL = None
from flask_socketio import SocketIO
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import secrets
import re
from datetime import datetime, timedelta
from functools import wraps
import gzip
from io import BytesIO

app = Flask(__name__, static_folder='static', static_url_path='/static')

# ─── Security Configuration ───────────────────────────────────────
# Generate secure secret key if not provided
if os.environ.get('PRODUCTION'):
    app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
else:
    app.secret_key = 'learnloop_secret_2024_dev'

# Security headers
@app.after_request
def set_security_headers(response):
    try:
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        # Enable XSS protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        # Content Security Policy
        response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' 'unsafe-eval' https://fonts.googleapis.com https://fonts.gstatic.com https://cdn.socket.io; img-src 'self' data: https:; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.socket.io;"
        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        # HTTPS enforcement in production
        if os.environ.get('PRODUCTION'):
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # Cache static assets for better performance
        if request.path.startswith('/static/'):
            # Cache CSS, JS, images for 7 days
            if any(request.path.endswith(ext) for ext in ['.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.woff', '.woff2']):
                response.headers['Cache-Control'] = 'public, max-age=604800'  # 7 days
        else:
            # Don't cache dynamic pages
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
    except Exception as e:
        # Log error but don't break the response
        print(f"Error in after_request: {e}")
    
    return response

# Session configuration
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('PRODUCTION', False)  # HTTPS only in production
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Session expires after 7 days

# File upload security
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# ─── Production/Development Config ────────────────────────────────
# Use environment variables in production, local config in development
if os.environ.get('PRODUCTION'):
    # Production configuration (shared hosting, Render, etc.)
    app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'sql12.freesqldatabase.com')
    app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'sql12817859')
    app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '')
    app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'sql12817859')
    app.secret_key = os.environ.get('SECRET_KEY', 'learnloop_secret_2024')
    app.config['DEBUG'] = False
else:
    # Development configuration (using remote database)
    app.config['MYSQL_HOST'] = 'sql12.freesqldatabase.com'
    app.config['MYSQL_USER'] = 'sql12817859'
    app.config['MYSQL_PASSWORD'] = 'YrEicfMveQ'
    app.config['MYSQL_DB'] = 'sql12817859'
    app.secret_key = 'learnloop_secret_2024'
    app.config['DEBUG'] = True

# Initialize SocketIO (use threading for PythonAnywhere compatibility)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Initialize MySQL (will be None if not configured)
try:
    if MySQL:
        print("🔄 Attempting to initialize MySQL connection...")
        print(f"   Host: {app.config.get('MYSQL_HOST')}")
        print(f"   User: {app.config.get('MYSQL_USER')}")
        print(f"   DB: {app.config.get('MYSQL_DB')}")
        mysql = MySQL(app)
        DB_AVAILABLE = True
        print("✅ MySQL connection initialized successfully")
    else:
        mysql = None
        DB_AVAILABLE = False
        print("⚠️  Flask-MySQLdb not installed")
except Exception as e:
    mysql = None
    DB_AVAILABLE = False
    print("❌ MySQL initialization failed:")
    print(f"   Error: {str(e)}")
    print("⚠️  Running in DEMO MODE ONLY")
    print("   To enable full features, setup MySQL database")

# ─── Simple Query Cache ───────────────────────────────────────────
from datetime import datetime as dt
query_cache = {}
CACHE_TTL = 300  # 5 minutes

def get_cached_query(key):
    """Get cached query result if not expired"""
    if key in query_cache:
        cached_data, timestamp = query_cache[key]
        if (dt.now() - timestamp).total_seconds() < CACHE_TTL:
            return cached_data
        else:
            del query_cache[key]
    return None

def set_cached_query(key, data):
    """Cache query result with timestamp"""
    query_cache[key] = (data, dt.now())

def clear_cache_pattern(pattern):
    """Clear cache entries matching pattern"""
    keys_to_delete = [k for k in query_cache.keys() if pattern in k]
    for key in keys_to_delete:
        del query_cache[key]

# ─── File Upload Config ───────────────────────────────────────────
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'docx', 'pptx'}
ALLOWED_MIME_TYPES = {
    'pdf': 'application/pdf',
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_filename(filename):
    """Sanitize filename to prevent directory traversal and other attacks"""
    # Remove any path components
    filename = os.path.basename(filename)
    # Use werkzeug's secure_filename
    filename = secure_filename(filename)
    # Add timestamp to prevent overwrites
    name, ext = os.path.splitext(filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{name}_{timestamp}{ext}"

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

def sanitize_input(text, max_length=1000):
    """Sanitize user input to prevent XSS"""
    if not text:
        return text
    # Remove any HTML tags
    text = re.sub(r'<[^>]*>', '', str(text))
    # Limit length
    text = text[:max_length]
    return text.strip()

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            # If no database, redirect to demo mode
            if not DB_AVAILABLE:
                flash('Database not configured. Redirecting to demo mode...', 'info')
                return redirect('/demo')
            flash('Please login first!', 'warning')
            return redirect('/login')
        
        # Check session expiry
        if 'last_activity' in session:
            last_activity = datetime.fromisoformat(session['last_activity'])
            if datetime.now() - last_activity > timedelta(hours=24):
                session.clear()
                flash('Session expired. Please login again.', 'warning')
                return redirect('/login')
        
        # Update last activity
        session['last_activity'] = datetime.now().isoformat()
        return f(*args, **kwargs)
    return decorated

def rate_limit_check(key, max_attempts=5, window_minutes=15):
    """Simple rate limiting"""
    if key not in session:
        session[key] = {'count': 0, 'timestamp': datetime.now().isoformat()}
    
    data = session[key]
    timestamp = datetime.fromisoformat(data['timestamp'])
    
    # Reset if window expired
    if datetime.now() - timestamp > timedelta(minutes=window_minutes):
        session[key] = {'count': 1, 'timestamp': datetime.now().isoformat()}
        return True
    
    # Check if limit exceeded
    if data['count'] >= max_attempts:
        return False
    
    # Increment counter
    data['count'] += 1
    session[key] = data
    return True

# ─── DEMO DATA ────────────────────────────────────────────────────
DEMO_DATA = {
    'user': {
        'id': 999,
        'name': 'Demo User',
        'email': 'demo@learnloop.com',
        'semester': 3,
        'college': '',
        'bio': 'This is a demo account. Explore all features!'
    },
    'groups': [
        (1, '🐍 Python Warriors', 'Python Programming', 3, 'Study group for Python unit tests, assignments and projects', 999, None, 6),
        (2, '🗄️ DBMS Masters', 'Database Management', 3, 'SQL queries, ER diagrams, normalization practice', 999, None, 8),
        (3, '💻 OS Study Circle', 'Operating Systems', 3, 'Process scheduling, memory management, exam prep', 999, None, 5),
        (4, '🔢 Maths Problem Solvers', 'Discrete Mathematics', 3, 'Graph theory, logic, sets and combinatorics', 999, None, 4),
    ],
    'students': [
        (1, 'Priya Singh', '', 3, 'Love Python and Web Development. Looking for partners for assignments.'),
        (2, 'Amit Verma', '', 3, 'Strong in DBMS and algorithms. Can help with database queries.'),
        (3, 'Neha Gupta', '', 3, 'Good at Operating Systems and Discrete Maths. Morning study sessions.'),
        (4, 'Rohit Kumar', '', 3, 'Interested in AI and Machine Learning. Notes sharing enthusiast.'),
        (5, 'Sneha Yadav', '', 3, 'Loves C++ and Data Structures. Night owl study sessions preferred.'),
        (6, 'Vivek Sharma', '', 3, 'Frontend developer in making. Good at HTML, CSS, JavaScript basics.'),
    ],
    'members': [
        (999, 'Demo User', 3, ''),
        (1, 'Priya Singh', 3, ''),
        (2, 'Amit Verma', 3, ''),
        (3, 'Neha Gupta', 3, 'Invertis University'),
        (4, 'Rohit Kumar', 3, 'Invertis University'),
        (5, 'Sneha Yadav', 3, 'Invertis University'),
    ],
    'messages': [
        (1, 1, 1, 'Hey everyone! Has anyone finished the Python assignment 3? 🤔', None, 'Priya Singh'),
        (2, 1, 999, 'Yes! Just finished it. Uploading the solution PDF now.', None, 'Demo User'),
        (3, 1, 2, 'Great! Also, can someone explain list comprehension? I\'m stuck on that 😅', None, 'Amit Verma'),
        (4, 1, 3, 'It\'s like a shortcut for loops! e.g. [x**2 for x in range(5)] gives [0, 1, 4, 9, 16] 🎯', None, 'Neha Gupta'),
        (5, 1, 999, 'Exactly what Neha said! Let\'s plan a study session this Saturday? 📅', None, 'Demo User'),
        (6, 1, 1, 'Saturday works for me! 10 AM at the library? 👍', None, 'Priya Singh'),
        (7, 1, 4, 'Count me in! 🙋', None, 'Rohit Kumar'),
    ],
    'notes': [
        (1, 1, 1, 'Python Unit 3 Notes.pdf', 'python_unit3.pdf', 'static/uploads/python_unit3.pdf', None, 'Priya Singh', 'Python Warriors'),
        (2, 1, 2, 'Functions & Modules.pdf', 'functions.pdf', 'static/uploads/functions.pdf', None, 'Amit Verma', 'Python Warriors'),
        (3, 2, 3, 'DBMS ER Diagram.pdf', 'er_diagram.pdf', 'static/uploads/er_diagram.pdf', None, 'Neha Gupta', 'DBMS Masters'),
    ]
}

# ─── HOME ─────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html', db_available=DB_AVAILABLE)

# ─── HEALTH CHECK ─────────────────────────────────────────────────
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'ok',
        'db_available': DB_AVAILABLE,
        'static_folder': app.static_folder,
        'static_url_path': app.static_url_path
    })

# ─── ABOUT ────────────────────────────────────────────────────────
@app.route('/about')
def about():
    return render_template('about.html')

# ─── FEATURES ─────────────────────────────────────────────────────
@app.route('/features')
def features():
    return render_template('features.html')

# ─── CONTACT ──────────────────────────────────────────────────────
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message_type = request.form.get('type')
    message = request.form.get('message')
    
    # In a real app, you would save this to a database or send an email
    # For now, just flash a success message
    flash(f'Thank you {name}! Your message has been received. We\'ll get back to you at {email} soon.', 'success')
    return redirect('/contact')

# ─── DEMO MODE ────────────────────────────────────────────────────
@app.route('/demo')
def demo_mode():
    # Set demo session
    session['demo_mode'] = True
    session['user_id'] = DEMO_DATA['user']['id']
    session['user_name'] = DEMO_DATA['user']['name']
    session['semester'] = DEMO_DATA['user']['semester']
    flash('🎭 Demo Mode Active - Explore all features!', 'info')
    return redirect('/dashboard')

@app.route('/exit-demo')
def exit_demo():
    session.clear()
    flash('Demo mode ended. Create an account to save your data!', 'info')
    return redirect('/')

# ─── REGISTER ─────────────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if not DB_AVAILABLE:
        flash('⚠️ Database connection error. Please try again later or contact support.', 'danger')
        return render_template('register.html')
    
    if request.method == 'POST':
        # Rate limiting
        if not rate_limit_check('register_attempts', max_attempts=3, window_minutes=60):
            flash('Too many registration attempts. Please try again later.', 'danger')
            return render_template('register.html')
        
        # Get and sanitize inputs
        name     = sanitize_input(request.form.get('name', ''), max_length=100)
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        semester = request.form.get('semester', '')
        college  = sanitize_input(request.form.get('college', ''), max_length=200)
        bio      = sanitize_input(request.form.get('bio', ''), max_length=500)
        
        # Validate inputs
        if not name or not email or not password:
            flash('All required fields must be filled!', 'danger')
            return render_template('register.html')
        
        if not validate_email(email):
            flash('Invalid email format!', 'danger')
            return render_template('register.html')
        
        is_valid, message = validate_password(password)
        if not is_valid:
            flash(message, 'danger')
            return render_template('register.html')
        
        # Hash password
        password_hash = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE email=%s", [email])
        if cur.fetchone():
            flash('Email already registered!', 'danger')
            return render_template('register.html')

        cur.execute("""INSERT INTO users (name, email, password, semester, college, bio)
                       VALUES (%s,%s,%s,%s,%s,%s)""",
                    (name, email, password_hash, semester, college, bio))
        mysql.connection.commit()
        cur.close()
        flash('Account created! Please login.', 'success')
        return redirect('/login')
    return render_template('register.html')

# ─── LOGIN ────────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if not DB_AVAILABLE:
        flash('⚠️ Database connection error. Please try again later or contact support.', 'danger')
        return render_template('login.html')
    
    if request.method == 'POST':
        # Rate limiting for login attempts
        if not rate_limit_check('login_attempts', max_attempts=5, window_minutes=15):
            flash('Too many login attempts. Please try again in 15 minutes.', 'danger')
            return render_template('login.html')
        
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email and password are required!', 'danger')
            return render_template('login.html')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", [email])
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], password):
            # Clear rate limit on successful login
            if 'login_attempts' in session:
                del session['login_attempts']
            
            # Set session data
            session.permanent = True
            session['user_id']   = user[0]
            session['user_name'] = user[1]
            session['semester']  = user[4]
            session['profile_picture'] = user[7] if len(user) > 7 else None  # profile_picture column
            session['last_activity'] = datetime.now().isoformat()
            
            flash(f'Welcome back, {user[1]}!', 'success')
            return redirect('/dashboard')
        flash('Invalid email or password!', 'danger')
    return render_template('login.html')

# ─── LOGOUT ───────────────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect('/')

# ─── FORGOT PASSWORD ──────────────────────────────────────────────
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if not DB_AVAILABLE:
        flash('⚠️ Database not configured. This feature is not available.', 'warning')
        return redirect('/login')
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        
        if not email:
            flash('Email is required!', 'danger')
            return render_template('forgot_password.html')
        
        # Check if user exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name FROM users WHERE email=%s", [email])
        user = cur.fetchone()
        
        if user:
            # Generate 6-digit OTP
            import random
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            
            # Calculate expiry time (10 minutes from now)
            from datetime import datetime, timedelta
            expires_at = datetime.now() + timedelta(minutes=10)
            
            # Store OTP in database
            cur.execute("""
                INSERT INTO password_reset_otps (email, otp, expires_at) 
                VALUES (%s, %s, %s)
            """, (email, otp, expires_at))
            mysql.connection.commit()
            
            # In production, send email here
            # For now, we'll show it in flash message (for testing)
            flash(f'OTP sent to {email}! Your OTP is: {otp} (Valid for 10 minutes)', 'success')
            
            # Store email in session for verification
            session['reset_email'] = email
            
            cur.close()
            return redirect('/verify-otp')
        else:
            # Don't reveal if email exists or not (security)
            flash(f'If an account exists with {email}, an OTP has been sent.', 'info')
        
        cur.close()
    
    return render_template('forgot_password.html')

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if not DB_AVAILABLE:
        flash('⚠️ Database not configured.', 'warning')
        return redirect('/login')
    
    email = session.get('reset_email')
    if not email:
        flash('Please request a password reset first.', 'warning')
        return redirect('/forgot-password')
    
    if request.method == 'POST':
        # Combine OTP digits
        otp = ''.join([
            request.form.get('otp1', ''),
            request.form.get('otp2', ''),
            request.form.get('otp3', ''),
            request.form.get('otp4', ''),
            request.form.get('otp5', ''),
            request.form.get('otp6', '')
        ])
        
        if len(otp) != 6:
            flash('Please enter all 6 digits!', 'danger')
            return render_template('verify_otp.html', email=email)
        
        # Verify OTP
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT id FROM password_reset_otps 
            WHERE email=%s AND otp=%s AND used=FALSE AND expires_at > NOW()
            ORDER BY created_at DESC LIMIT 1
        """, (email, otp))
        otp_record = cur.fetchone()
        
        if otp_record:
            # Mark OTP as used
            cur.execute("UPDATE password_reset_otps SET used=TRUE WHERE id=%s", [otp_record[0]])
            mysql.connection.commit()
            cur.close()
            
            # Store verification in session
            session['otp_verified'] = True
            flash('OTP verified successfully! Set your new password.', 'success')
            return redirect('/reset-password')
        else:
            cur.close()
            flash('Invalid or expired OTP. Please try again.', 'danger')
    
    return render_template('verify_otp.html', email=email)

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if not DB_AVAILABLE:
        flash('⚠️ Database not configured.', 'warning')
        return redirect('/login')
    
    email = session.get('reset_email')
    otp_verified = session.get('otp_verified')
    
    if not email or not otp_verified:
        flash('Please complete OTP verification first.', 'warning')
        return redirect('/forgot-password')
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not password or not confirm_password:
            flash('Both password fields are required!', 'danger')
            return render_template('reset_password.html', email=email)
        
        if len(password) < 6:
            flash('Password must be at least 6 characters!', 'danger')
            return render_template('reset_password.html', email=email)
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('reset_password.html', email=email)
        
        # Update password
        hashed_password = generate_password_hash(password)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET password=%s WHERE email=%s", (hashed_password, email))
        mysql.connection.commit()
        cur.close()
        
        # Clear session
        session.pop('reset_email', None)
        session.pop('otp_verified', None)
        
        flash('Password reset successfully! You can now login with your new password.', 'success')
        return redirect('/login')
    
    return render_template('reset_password.html', email=email)

@app.route('/resend-otp')
def resend_otp():
    if not DB_AVAILABLE:
        flash('⚠️ Database not configured.', 'warning')
        return redirect('/login')
    
    email = request.args.get('email') or session.get('reset_email')
    
    if not email:
        flash('Invalid request.', 'danger')
        return redirect('/forgot-password')
    
    # Generate new OTP
    import random
    from datetime import datetime, timedelta
    
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    expires_at = datetime.now() + timedelta(minutes=10)
    
    # Store new OTP
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO password_reset_otps (email, otp, expires_at) 
        VALUES (%s, %s, %s)
    """, (email, otp, expires_at))
    mysql.connection.commit()
    cur.close()
    
    # In production, send email here
    flash(f'New OTP sent! Your OTP is: {otp} (Valid for 10 minutes)', 'success')
    
    session['reset_email'] = email
    return redirect('/verify-otp')

# ─── DASHBOARD ────────────────────────────────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    # Check if demo mode
    if session.get('demo_mode'):
        my_groups = DEMO_DATA['groups']
        suggestions = DEMO_DATA['students'][:3]
        recent_notes = DEMO_DATA['notes'][:3]
    else:
        cur = mysql.connection.cursor()

        # My groups
        cur.execute("""SELECT g.* FROM `groups` g
                       JOIN group_members gm ON g.id = gm.group_id
                       WHERE gm.user_id = %s""", [session['user_id']])
        my_groups = cur.fetchall()

        # Suggested partners (same semester, not self)
        cur.execute("""SELECT id, name, college, semester, bio FROM users
                       WHERE semester=%s AND id != %s LIMIT 6""",
                    [session['semester'], session['user_id']])
        suggestions = cur.fetchall()

        # Recent notes
        cur.execute("""SELECT n.*, u.name as uploader, g.group_name FROM notes n
                       JOIN users u ON n.uploaded_by = u.id
                       JOIN `groups` g ON n.group_id = g.id
                       JOIN group_members gm ON g.id = gm.group_id
                       WHERE gm.user_id = %s
                       ORDER BY n.uploaded_at DESC LIMIT 5""", [session['user_id']])
        recent_notes = cur.fetchall()

    return render_template('dashboard.html',
                           my_groups=my_groups,
                           suggestions=suggestions,
                           recent_notes=recent_notes)

# ─── FIND PARTNERS ────────────────────────────────────────────────
@app.route('/find-partners')
@login_required
def find_partners():
    topic = request.args.get('topic', '')
    language = request.args.get('language', '')

    if session.get('demo_mode'):
        students = DEMO_DATA['students']
        # Simple filtering for demo
        if topic:
            students = [s for s in students if topic.lower() in (s[4] or '').lower()]
        if language:
            students = [s for s in students if language.lower() in (s[2] or '').lower()]
    else:
        cur = mysql.connection.cursor()
        query = "SELECT id, name, college, semester, bio FROM users WHERE id != %s"
        params = [session['user_id']]

        if topic:
            query += " AND (bio LIKE %s OR college LIKE %s)"
            params.append(f'%{topic}%')
            params.append(f'%{topic}%')
        if language:
            query += " AND (bio LIKE %s OR college LIKE %s)"
            params.append(f'%{language}%')
            params.append(f'%{language}%')

        cur.execute(query, params)
        students = cur.fetchall()
        cur.close()
    
    return render_template('find_partners.html', students=students,
                           topic=topic, language=language)

# ─── CREATE GROUP ─────────────────────────────────────────────────
@app.route('/create-group', methods=['GET', 'POST'])
@login_required
def create_group():
    if session.get('demo_mode'):
        flash('⚠️ Demo Mode: Group creation is disabled. Sign up to create real groups!', 'warning')
        return redirect('/groups')
    
    if request.method == 'POST':
        group_name  = request.form['group_name']
        subject     = request.form['subject']
        semester    = request.form['semester']
        description = request.form.get('description', '')
        is_public   = request.form.get('is_public', 'on') == 'on'  # Default to public

        cur = mysql.connection.cursor()
        cur.execute("""INSERT INTO `groups` (group_name, subject, semester, description, created_by, is_public)
                       VALUES (%s,%s,%s,%s,%s,%s)""",
                    (group_name, subject, semester, description, session['user_id'], is_public))
        mysql.connection.commit()
        group_id = cur.lastrowid

        # Auto-add creator as member
        cur.execute("INSERT INTO group_members (group_id, user_id) VALUES (%s,%s)",
                    (group_id, session['user_id']))
        mysql.connection.commit()
        
        # Send notifications to users studying the same subject
        if is_public:
            # Find users with same subject in their bio or studying same semester
            cur.execute("""
                SELECT DISTINCT u.id, u.name 
                FROM users u
                WHERE u.id != %s 
                AND (
                    u.bio LIKE %s 
                    OR u.semester = %s
                )
                LIMIT 50
            """, [session['user_id'], f'%{subject}%', semester])
            
            potential_members = cur.fetchall()
            
            # Create notifications for these users
            notification_title = f"New {subject} Study Group!"
            notification_message = f"{session['user_name']} created '{group_name}' for {subject} (Semester {semester}). Join now!"
            
            for user in potential_members:
                cur.execute("""
                    INSERT INTO notifications (user_id, type, title, message, link)
                    VALUES (%s, 'group_created', %s, %s, %s)
                """, [user[0], notification_title, notification_message, f'/group/{group_id}'])
            
            mysql.connection.commit()
            
            if len(potential_members) > 0:
                flash(f'Group created! {len(potential_members)} students notified.', 'success')
            else:
                flash('Group created successfully!', 'success')
        else:
            flash('Private group created successfully!', 'success')
        
        cur.close()
        return redirect(f'/group/{group_id}')
    return render_template('create_group.html')

# ─── VIEW GROUP ───────────────────────────────────────────────────
@app.route('/group/<int:group_id>')
@login_required
def view_group(group_id):
    if session.get('demo_mode'):
        # Find group in demo data
        group = next((g for g in DEMO_DATA['groups'] if g[0] == group_id), None)
        if not group:
            flash('Group not found!', 'danger')
            return redirect('/dashboard')
        
        is_member = True  # Demo user is member of all groups
        members = DEMO_DATA['members']
        notes = DEMO_DATA['notes']
        messages = DEMO_DATA['messages']
    else:
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM `groups` WHERE id=%s", [group_id])
        group = cur.fetchone()
        if not group:
            flash('Group not found!', 'danger')
            return redirect('/dashboard')

        # Check membership
        cur.execute("SELECT id FROM group_members WHERE group_id=%s AND user_id=%s",
                    [group_id, session['user_id']])
        is_member = cur.fetchone()

        # Members
        cur.execute("""SELECT u.id, u.name, u.semester, u.college FROM users u
                       JOIN group_members gm ON u.id = gm.user_id
                       WHERE gm.group_id = %s""", [group_id])
        members = cur.fetchall()

        # Notes
        cur.execute("""SELECT n.*, u.name as uploader FROM notes n
                       JOIN users u ON n.uploaded_by = u.id
                       WHERE n.group_id = %s ORDER BY n.uploaded_at DESC""", [group_id])
        notes = cur.fetchall()

        # Messages
        cur.execute("""SELECT m.*, u.name as sender FROM messages m
                       JOIN users u ON m.user_id = u.id
                       WHERE m.group_id = %s ORDER BY m.sent_at ASC""", [group_id])
        messages = cur.fetchall()

    return render_template('group.html', group=group, members=members,
                           notes=notes, messages=messages, is_member=is_member)

# ─── JOIN GROUP ───────────────────────────────────────────────────
@app.route('/join-group/<int:group_id>')
@login_required
def join_group(group_id):
    if session.get('demo_mode'):
        flash('⚠️ Demo Mode: Joining groups is disabled. Sign up for full access!', 'warning')
        return redirect(f'/group/{group_id}')
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM group_members WHERE group_id=%s AND user_id=%s",
                [group_id, session['user_id']])
    if not cur.fetchone():
        cur.execute("INSERT INTO group_members (group_id, user_id) VALUES (%s,%s)",
                    (group_id, session['user_id']))
        mysql.connection.commit()
        flash('Joined group!', 'success')
    return redirect(f'/group/{group_id}')

# ─── LEAVE GROUP ──────────────────────────────────────────────────
@app.route('/leave-group/<int:group_id>', methods=['POST'])
@login_required
def leave_group(group_id):
    if session.get('demo_mode'):
        return jsonify({'error': 'Demo mode'}), 403
    
    cur = mysql.connection.cursor()
    
    # Check if user is the creator
    cur.execute("SELECT created_by FROM `groups` WHERE id=%s", [group_id])
    group = cur.fetchone()
    
    if group and group[0] == session['user_id']:
        return jsonify({'error': 'Creator cannot leave the group. Delete it instead.'}), 403
    
    # Remove user from group
    cur.execute("DELETE FROM group_members WHERE group_id=%s AND user_id=%s",
                (group_id, session['user_id']))
    mysql.connection.commit()
    
    return jsonify({'success': True})

# ─── EDIT GROUP ───────────────────────────────────────────────────
@app.route('/edit-group/<int:group_id>', methods=['GET', 'POST'])
@login_required
def edit_group(group_id):
    if session.get('demo_mode'):
        flash('⚠️ Demo Mode: Editing is disabled. Sign up for full access!', 'warning')
        return redirect(f'/group/{group_id}')
    
    cur = mysql.connection.cursor()
    
    # Get group and verify creator
    cur.execute("SELECT * FROM `groups` WHERE id=%s", [group_id])
    group = cur.fetchone()
    
    if not group:
        flash('Group not found!', 'danger')
        return redirect('/groups')
    
    if group[5] != session['user_id']:  # created_by field
        flash('Only the creator can edit this group!', 'danger')
        return redirect(f'/group/{group_id}')
    
    if request.method == 'POST':
        group_name = request.form['group_name']
        subject = request.form['subject']
        semester = request.form['semester']
        description = request.form.get('description', '')
        
        cur.execute("""
            UPDATE `groups` 
            SET group_name=%s, subject=%s, semester=%s, description=%s
            WHERE id=%s
        """, (group_name, subject, semester, description, group_id))
        mysql.connection.commit()
        
        flash('Group updated successfully!', 'success')
        return redirect(f'/group/{group_id}')
    
    return render_template('edit_group.html', group=group)

# ─── DELETE GROUP ─────────────────────────────────────────────────
@app.route('/delete-group/<int:group_id>', methods=['POST'])
@login_required
def delete_group(group_id):
    if session.get('demo_mode'):
        return jsonify({'error': 'Demo mode'}), 403
    
    cur = mysql.connection.cursor()
    
    try:
        # Verify user is creator
        cur.execute("SELECT created_by FROM `groups` WHERE id=%s", [group_id])
        group = cur.fetchone()
        
        if not group:
            cur.close()
            return jsonify({'error': 'Group not found'}), 404
        
        if group[0] != session['user_id']:
            cur.close()
            return jsonify({'error': 'Only the creator can delete this group'}), 403
        
        # Delete related records first (foreign key constraints)
        cur.execute("DELETE FROM messages WHERE group_id=%s", [group_id])
        cur.execute("DELETE FROM notes WHERE group_id=%s", [group_id])
        cur.execute("DELETE FROM group_members WHERE group_id=%s", [group_id])
        
        # Delete the group
        cur.execute("DELETE FROM `groups` WHERE id=%s", [group_id])
        
        mysql.connection.commit()
        cur.close()
        
        return jsonify({'success': True})
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        print(f"Error deleting group: {e}")
        return jsonify({'error': str(e)}), 500

# ─── ALL GROUPS ───────────────────────────────────────────────────
@app.route('/groups')
@login_required
def all_groups():
    semester = request.args.get('semester', '')
    subject  = request.args.get('subject', '')
    show_all = request.args.get('show_all', '') == 'true'

    if session.get('demo_mode'):
        groups = DEMO_DATA['groups']
        # Simple filtering for demo
        if semester:
            groups = [g for g in groups if str(g[3]) == semester]
        if subject:
            groups = [g for g in groups if subject.lower() in g[2].lower()]
    else:
        cur = mysql.connection.cursor()
        query = """SELECT g.*, u.name as creator,
                   (SELECT COUNT(*) FROM group_members WHERE group_id=g.id) as member_count
                   FROM `groups` g JOIN users u ON g.created_by = u.id 
                   WHERE 1=1"""
        params = []
        
        # Show only public groups unless user wants to see all
        if not show_all:
            query += " AND g.is_public = TRUE"
        
        if semester:
            query += " AND g.semester=%s"
            params.append(semester)
        if subject:
            query += " AND g.subject LIKE %s"
            params.append(f'%{subject}%')
        query += " ORDER BY g.created_at DESC"

        cur.execute(query, params)
        groups = cur.fetchall()
        cur.close()
    
    return render_template('groups.html', groups=groups, semester=semester, subject=subject, show_all=show_all)

# ─── UPLOAD NOTE ──────────────────────────────────────────────────
@app.route('/upload-note/<int:group_id>', methods=['POST'])
@login_required
def upload_note(group_id):
    if session.get('demo_mode'):
        flash('⚠️ Demo Mode: File uploads are disabled. Sign up to upload real files!', 'warning')
        return redirect(f'/group/{group_id}')
    
    if 'file' not in request.files:
        flash('No file selected!', 'danger')
        return redirect(f'/group/{group_id}')

    file = request.files['file']
    title = request.form.get('title', file.filename)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        cur = mysql.connection.cursor()
        cur.execute("""INSERT INTO notes (group_id, uploaded_by, title, file_name, file_path)
                       VALUES (%s,%s,%s,%s,%s)""",
                    (group_id, session['user_id'], title, filename, filepath))
        mysql.connection.commit()
        flash('Note uploaded!', 'success')
    else:
        flash('Invalid file type!', 'danger')
    return redirect(f'/group/{group_id}')

# ─── DOWNLOAD FILE ────────────────────────────────────────────────
@app.route('/download/<path:filename>')
@login_required
def download_file(filename):
    """Download a file from uploads folder"""
    from flask import send_from_directory
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        flash('File not found!', 'danger')
        return redirect('/dashboard')

# ─── SEND MESSAGE ─────────────────────────────────────────────────
@app.route('/send-message/<int:group_id>', methods=['POST'])
@login_required
def send_message(group_id):
    if session.get('demo_mode'):
        flash('⚠️ Demo Mode: Messaging is disabled. Sign up to send real messages!', 'warning')
        return redirect(f'/group/{group_id}')
    
    message = request.form.get('message', '').strip()
    if message:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO messages (group_id, user_id, message) VALUES (%s,%s,%s)",
                    (group_id, session['user_id'], message))
        mysql.connection.commit()
    return redirect(f'/group/{group_id}')

# ─── PROFILE ──────────────────────────────────────────────────────
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name     = request.form['name']
        semester = request.form['semester']
        college  = request.form['college']
        bio      = request.form.get('bio', '')
        cur.execute("""UPDATE users SET name=%s, semester=%s, college=%s, bio=%s
                       WHERE id=%s""",
                    (name, semester, college, bio, session['user_id']))
        mysql.connection.commit()
        session['user_name'] = name
        session['semester']  = semester
        flash('Profile updated!', 'success')

    cur.execute("SELECT * FROM users WHERE id=%s", [session['user_id']])
    user = cur.fetchone()
    cur.close()
    return render_template('profile.html', user=user)

@app.route('/view-profile/<int:user_id>')
@login_required
def view_profile(user_id):
    """View another user's profile"""
    cur = mysql.connection.cursor()
    
    # Get user info
    cur.execute("SELECT id, name, email, semester, college, bio, created_at, profile_picture FROM users WHERE id=%s", [user_id])
    user = cur.fetchone()
    
    if not user:
        flash('User not found', 'error')
        return redirect('/find-partners')
    
    # Check friendship status
    cur.execute("""
        SELECT status FROM friendships 
        WHERE (user_id = %s AND friend_id = %s) OR (user_id = %s AND friend_id = %s)
    """, [session['user_id'], user_id, user_id, session['user_id']])
    
    friendship = cur.fetchone()
    friendship_status = friendship[0] if friendship else None
    
    # Check if current user sent the request
    cur.execute("""
        SELECT user_id FROM friendships 
        WHERE user_id = %s AND friend_id = %s
    """, [session['user_id'], user_id])
    
    is_requester = cur.fetchone() is not None
    
    # Get user's groups
    cur.execute("""
        SELECT g.id, g.group_name, g.subject, g.semester
        FROM `groups` g
        WHERE g.created_by = %s
        ORDER BY g.created_at DESC
        LIMIT 5
    """, [user_id])
    
    groups = cur.fetchall()
    
    cur.close()
    
    return render_template('view_profile.html', 
                         user=user, 
                         friendship_status=friendship_status,
                         is_requester=is_requester,
                         groups=groups,
                         is_own_profile=(user_id == session['user_id']))

@app.route('/upload-profile-picture', methods=['POST'])
@login_required
def upload_profile_picture():
    try:
        print(f"Upload request received from user {session.get('user_id')}")
        print(f"Files in request: {list(request.files.keys())}")
        
        if 'profile_picture' not in request.files:
            print("Error: No profile_picture in request.files")
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['profile_picture']
        print(f"File received: {file.filename}")
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_ext not in allowed_extensions:
            return jsonify({'error': 'Invalid file type. Use PNG, JPG, JPEG, GIF, or WEBP'}), 400
        
        if file:
            import os
            from werkzeug.utils import secure_filename
            
            # Create uploads directory if it doesn't exist
            upload_folder = os.path.join('static', 'uploads', 'profiles')
            os.makedirs(upload_folder, exist_ok=True)
            print(f"Upload folder: {upload_folder}")
            
            # Generate unique filename
            filename = secure_filename(f"user_{session['user_id']}_{file.filename}")
            filepath = os.path.join(upload_folder, filename)
            print(f"Saving to: {filepath}")
            
            # Save file
            file.save(filepath)
            print(f"File saved successfully")
            
            # Update database
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET profile_picture=%s WHERE id=%s", 
                       (filename, session['user_id']))
            mysql.connection.commit()
            cur.close()
            print(f"Database updated successfully")
            
            return jsonify({
                'success': True, 
                'filename': filename,
                'profile_picture_url': f'/static/uploads/profiles/{filename}'
            })
        
        return jsonify({'error': 'Upload failed'}), 500
    except Exception as e:
        import traceback
        print(f"Error uploading profile picture: {e}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/remove-profile-picture', methods=['POST'])
@login_required
def remove_profile_picture():
    try:
        # Update database to remove profile picture
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET profile_picture=NULL WHERE id=%s", [session['user_id']])
        mysql.connection.commit()
        cur.close()
        
        return jsonify({'success': True})
    except Exception as e:
        import traceback
        print(f"Error removing profile picture: {e}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

# ─── MESSAGING & FRIENDS ──────────────────────────────────────────

@app.route('/messages')
@login_required
def messages():
    """View all conversations"""
    cur = mysql.connection.cursor()
    
    # Get all friends (accepted friendships)
    cur.execute("""
        SELECT DISTINCT u.id, u.name, u.profile_picture,
               (SELECT COUNT(*) FROM direct_messages 
                WHERE sender_id = u.id AND receiver_id = %s AND is_read = FALSE) as unread_count,
               (SELECT message FROM direct_messages 
                WHERE (sender_id = u.id AND receiver_id = %s) OR (sender_id = %s AND receiver_id = u.id)
                ORDER BY sent_at DESC LIMIT 1) as last_message,
               (SELECT sent_at FROM direct_messages 
                WHERE (sender_id = u.id AND receiver_id = %s) OR (sender_id = %s AND receiver_id = u.id)
                ORDER BY sent_at DESC LIMIT 1) as last_message_time
        FROM users u
        WHERE u.id IN (
            SELECT friend_id FROM friendships WHERE user_id = %s AND status = 'accepted'
            UNION
            SELECT user_id FROM friendships WHERE friend_id = %s AND status = 'accepted'
        )
        ORDER BY last_message_time DESC
    """, [session['user_id'], session['user_id'], session['user_id'], 
          session['user_id'], session['user_id'], session['user_id'], session['user_id']])
    
    friends = cur.fetchall()
    
    # Get pending friend requests
    cur.execute("""
        SELECT u.id, u.name, u.profile_picture, f.created_at
        FROM friendships f
        JOIN users u ON f.user_id = u.id
        WHERE f.friend_id = %s AND f.status = 'pending'
        ORDER BY f.created_at DESC
    """, [session['user_id']])
    
    pending_requests = cur.fetchall()
    cur.close()
    
    return render_template('messages.html', friends=friends, pending_requests=pending_requests)

@app.route('/chat/<int:friend_id>')
@login_required
def chat(friend_id):
    """Chat with a specific friend"""
    cur = mysql.connection.cursor()
    
    # Verify friendship
    cur.execute("""
        SELECT * FROM friendships 
        WHERE ((user_id = %s AND friend_id = %s) OR (user_id = %s AND friend_id = %s))
        AND status = 'accepted'
    """, [session['user_id'], friend_id, friend_id, session['user_id']])
    
    friendship = cur.fetchone()
    
    if not friendship:
        flash('You are not friends with this user', 'error')
        return redirect('/messages')
    
    # Get friend info
    cur.execute("SELECT id, name, profile_picture, bio FROM users WHERE id = %s", [friend_id])
    friend = cur.fetchone()
    
    # Get chat messages
    cur.execute("""
        SELECT dm.*, u.name as sender_name
        FROM direct_messages dm
        JOIN users u ON dm.sender_id = u.id
        WHERE (dm.sender_id = %s AND dm.receiver_id = %s) 
           OR (dm.sender_id = %s AND dm.receiver_id = %s)
        ORDER BY dm.sent_at ASC
    """, [session['user_id'], friend_id, friend_id, session['user_id']])
    
    messages_list = cur.fetchall()
    
    # Mark messages as read
    cur.execute("""
        UPDATE direct_messages 
        SET is_read = TRUE 
        WHERE sender_id = %s AND receiver_id = %s AND is_read = FALSE
    """, [friend_id, session['user_id']])
    
    mysql.connection.commit()
    cur.close()
    
    return render_template('chat.html', friend=friend, messages=messages_list)

@app.route('/send-friend-request/<int:user_id>', methods=['POST'])
@login_required
def send_friend_request(user_id):
    """Send a friend request"""
    if user_id == session['user_id']:
        return jsonify({'error': 'Cannot send friend request to yourself'}), 400
    
    cur = mysql.connection.cursor()
    
    try:
        cur.execute("""
            INSERT INTO friendships (user_id, friend_id, status)
            VALUES (%s, %s, 'pending')
        """, [session['user_id'], user_id])
        
        mysql.connection.commit()
        cur.close()
        return jsonify({'success': True})
    except Exception as e:
        cur.close()
        return jsonify({'error': 'Friend request already sent or exists'}), 400

@app.route('/accept-friend-request/<int:user_id>', methods=['POST'])
@login_required
def accept_friend_request(user_id):
    """Accept a friend request"""
    cur = mysql.connection.cursor()
    
    cur.execute("""
        UPDATE friendships 
        SET status = 'accepted' 
        WHERE user_id = %s AND friend_id = %s AND status = 'pending'
    """, [user_id, session['user_id']])
    
    mysql.connection.commit()
    cur.close()
    
    return jsonify({'success': True})

@app.route('/reject-friend-request/<int:user_id>', methods=['POST'])
@login_required
def reject_friend_request(user_id):
    """Reject a friend request"""
    cur = mysql.connection.cursor()
    
    cur.execute("""
        DELETE FROM friendships 
        WHERE user_id = %s AND friend_id = %s AND status = 'pending'
    """, [user_id, session['user_id']])
    
    mysql.connection.commit()
    cur.close()
    
    return jsonify({'success': True})

@app.route('/send-direct-message/<int:friend_id>', methods=['POST'])
@login_required
def send_direct_message(friend_id):
    """Send a message to a friend"""
    message = request.form.get('message', '')
    file = request.files.get('file')
    
    cur = mysql.connection.cursor()
    
    try:
        file_name = None
        file_path = None
        file_type = 'other'
        
        if file and file.filename:
            import os
            from werkzeug.utils import secure_filename
            
            # Create uploads directory
            upload_folder = os.path.join('static', 'uploads', 'messages')
            os.makedirs(upload_folder, exist_ok=True)
            
            # Determine file type
            file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
            if file_ext == 'pdf':
                file_type = 'pdf'
            elif file_ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                file_type = 'image'
            elif file_ext in ['doc', 'docx', 'txt', 'xlsx', 'pptx']:
                file_type = 'document'
            
            # Save file
            file_name = secure_filename(f"{session['user_id']}_{friend_id}_{file.filename}")
            file_path = os.path.join(upload_folder, file_name)
            file.save(file_path)
            file_path = f"uploads/messages/{file_name}"
        
        # Insert message
        cur.execute("""
            INSERT INTO direct_messages (sender_id, receiver_id, message, file_name, file_path, file_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, [session['user_id'], friend_id, message, file_name, file_path, file_type])
        
        mysql.connection.commit()
        message_id = cur.lastrowid
        cur.close()
        
        # Emit socket event for real-time messaging
        socketio.emit('new_message', {
            'message_id': message_id,
            'sender_id': session['user_id'],
            'receiver_id': friend_id,
            'message': message,
            'file_name': file_name,
            'file_path': file_path,
            'file_type': file_type
        }, room=f'user_{friend_id}')
        
        return jsonify({'success': True, 'message_id': message_id})
    except Exception as e:
        cur.close()
        return jsonify({'error': str(e)}), 500

# ─── NOTIFICATIONS ────────────────────────────────────────────────

@app.route('/notifications')
@login_required
def notifications():
    """View all notifications"""
    cur = mysql.connection.cursor()
    
    # Get all notifications for current user
    cur.execute("""
        SELECT *
        FROM notifications
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 50
    """, [session['user_id']])
    
    notifications_list = cur.fetchall()
    
    # Get pending friend requests
    cur.execute("""
        SELECT u.id, u.name, u.profile_picture, f.created_at
        FROM friendships f
        JOIN users u ON f.user_id = u.id
        WHERE f.friend_id = %s AND f.status = 'pending'
        ORDER BY f.created_at DESC
    """, [session['user_id']])
    
    friend_requests = cur.fetchall()
    cur.close()
    
    return render_template('notifications.html', 
                         notifications=notifications_list,
                         friend_requests=friend_requests)

@app.route('/notifications/count')
@login_required
def notifications_count():
    """Get unread notification count"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM notifications WHERE user_id = %s AND is_read = FALSE", [session['user_id']])
    count = cur.fetchone()[0]
    cur.close()
    return jsonify({'count': count})

@app.route('/mark-notification-read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """Mark a notification as read"""
    cur = mysql.connection.cursor()
    cur.execute("UPDATE notifications SET is_read = TRUE WHERE id = %s AND user_id = %s", 
               [notification_id, session['user_id']])
    mysql.connection.commit()
    cur.close()
    return jsonify({'success': True})

@app.route('/mark-all-notifications-read', methods=['POST'])
@login_required
def mark_all_notifications_read():
    """Mark all notifications as read"""
    cur = mysql.connection.cursor()
    cur.execute("UPDATE notifications SET is_read = TRUE WHERE user_id = %s", [session['user_id']])
    mysql.connection.commit()
    cur.close()
    return jsonify({'success': True})

@app.route('/delete-notification/<int:notification_id>', methods=['POST'])
@login_required
def delete_notification(notification_id):
    """Delete a notification"""
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM notifications WHERE id = %s AND user_id = %s", 
               [notification_id, session['user_id']])
    mysql.connection.commit()
    cur.close()
    return jsonify({'success': True})

@app.route('/api/latest-notifications')
@login_required
def latest_notifications():
    """Get latest unread notifications for popup"""
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, user_id, type, title, message, link, is_read, created_at
        FROM notifications
        WHERE user_id = %s AND is_read = FALSE
        ORDER BY created_at DESC
        LIMIT 5
    """, [session['user_id']])
    
    notifications = cur.fetchall()
    cur.close()
    
    # Convert to list of dicts
    notif_list = []
    for notif in notifications:
        notif_list.append({
            'id': notif[0],
            'type': notif[2],
            'title': notif[3],
            'message': notif[4],
            'link': notif[5]
        })
    
    return jsonify({'notifications': notif_list})

# Import and register voice room routes (must be outside if __name__ for production)
from voice_room_routes import register_voice_room_routes
register_voice_room_routes(app, mysql, socketio)

if __name__ == '__main__':
    # Run on all network interfaces for mobile access
    # Access via: http://YOUR_IP:5000 from mobile on same WiFi
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

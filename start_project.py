"""
LearnLoop Project Launcher
Checks all prerequisites and starts the application
"""

import os
import sys
import subprocess
import time

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_mysql():
    """Check if MySQL is accessible"""
    print("\n🔍 Checking MySQL connection...")
    try:
        import MySQLdb
        conn = MySQLdb.connect(
            host='localhost',
            user='root',
            passwd='',
            db='learnloop'
        )
        conn.close()
        print("✅ MySQL is running and database is ready!")
        return True
    except MySQLdb.Error as e:
        print(f"❌ MySQL connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_dependencies():
    """Check if all Python packages are installed"""
    print("\n🔍 Checking dependencies...")
    required = ['flask', 'flask_mysqldb', 'werkzeug']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed!")
    return True

def check_uploads_folder():
    """Ensure uploads folder exists"""
    print("\n🔍 Checking uploads folder...")
    upload_path = os.path.join('static', 'uploads')
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        print(f"✅ Created uploads folder: {upload_path}")
    else:
        print(f"✅ Uploads folder exists: {upload_path}")
    return True

def main():
    print_header("LearnLoop Project Launcher")
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first!")
        sys.exit(1)
    
    # Check uploads folder
    check_uploads_folder()
    
    # Check MySQL
    mysql_ready = check_mysql()
    
    if not mysql_ready:
        print("\n" + "=" * 60)
        print("⚠️  MySQL NOT READY")
        print("=" * 60)
        print("\n📋 Setup Instructions:")
        print("\n1. Start XAMPP/MySQL:")
        print("   - Open XAMPP Control Panel")
        print("   - Click 'Start' for MySQL")
        print("   - Wait for green 'Running' status")
        print("\n2. Setup Database:")
        print("   Run: python setup_database.py")
        print("\n3. Test Connection:")
        print("   Run: python test_connection.py")
        print("\n4. Start Application:")
        print("   Run: python app.py")
        print("\n💡 OR use Demo Mode (no database needed):")
        print("   Run: python app.py")
        print("   Then visit: http://127.0.0.1:5000/demo")
        print("\n" + "=" * 60)
        
        choice = input("\nStart in Demo Mode anyway? (y/n): ").lower()
        if choice != 'y':
            sys.exit(1)
    
    # Start the application
    print_header("Starting LearnLoop Application")
    print("\n🚀 Launching Flask server...")
    print("📍 Access at: http://127.0.0.1:5000")
    
    if not mysql_ready:
        print("🎭 Demo Mode: Visit http://127.0.0.1:5000/demo")
    
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    try:
        # Start Flask app
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

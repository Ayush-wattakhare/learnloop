#!/usr/bin/env python3
"""
LearnLoop Deployment Readiness Verification Script
Run this before deploying to verify everything is ready
"""

import os
import sys

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_check(text, status):
    symbol = "✅" if status else "❌"
    print(f"{symbol} {text}")
    return status

def check_file_exists(filepath):
    return os.path.exists(filepath)

def main():
    print_header("LearnLoop Deployment Readiness Check")
    print("\nAs your senior developer, I'm verifying everything is ready...\n")
    
    all_checks_passed = True
    
    # Check core files
    print_header("1. Core Application Files")
    all_checks_passed &= print_check("app.py exists", check_file_exists("app.py"))
    all_checks_passed &= print_check("voice_room_routes.py exists", check_file_exists("voice_room_routes.py"))
    all_checks_passed &= print_check("requirements.txt exists", check_file_exists("requirements.txt"))
    all_checks_passed &= print_check("setup_learnloop_database.py exists", check_file_exists("setup_learnloop_database.py"))
    
    # Check templates
    print_header("2. Template Files")
    templates_exist = os.path.exists("templates") and os.path.isdir("templates")
    all_checks_passed &= print_check("templates/ folder exists", templates_exist)
    
    if templates_exist:
        required_templates = [
            "base.html", "index.html", "dashboard.html", "login.html", 
            "register.html", "groups.html", "messages.html", "voice_rooms.html"
        ]
        for template in required_templates:
            path = os.path.join("templates", template)
            all_checks_passed &= print_check(f"  {template}", check_file_exists(path))
    
    # Check static files
    print_header("3. Static Files")
    static_exists = os.path.exists("static") and os.path.isdir("static")
    all_checks_passed &= print_check("static/ folder exists", static_exists)
    
    if static_exists:
        all_checks_passed &= print_check("  static/css/ exists", check_file_exists("static/css"))
        all_checks_passed &= print_check("  static/css/style.css exists", check_file_exists("static/css/style.css"))
        
        # Check upload folders
        upload_folders = ["static/uploads", "static/uploads/profiles", 
                         "static/uploads/messages", "static/uploads/notes"]
        for folder in upload_folders:
            exists = os.path.exists(folder)
            if not exists:
                try:
                    os.makedirs(folder, exist_ok=True)
                    print_check(f"  {folder}/ created", True)
                except:
                    all_checks_passed &= print_check(f"  {folder}/ exists", False)
            else:
                print_check(f"  {folder}/ exists", True)
    
    # Check Python dependencies
    print_header("4. Python Dependencies")
    try:
        import flask
        print_check("Flask installed", True)
    except ImportError:
        all_checks_passed &= print_check("Flask installed", False)
        print("  → Run: pip install flask")
    
    try:
        import flask_mysqldb
        print_check("Flask-MySQLdb installed", True)
    except ImportError:
        all_checks_passed &= print_check("Flask-MySQLdb installed", False)
        print("  → Run: pip install flask-mysqldb")
    
    try:
        import flask_socketio
        print_check("Flask-SocketIO installed", True)
    except ImportError:
        all_checks_passed &= print_check("Flask-SocketIO installed", False)
        print("  → Run: pip install flask-socketio")
    
    try:
        import MySQLdb
        print_check("mysqlclient installed", True)
    except ImportError:
        all_checks_passed &= print_check("mysqlclient installed", False)
        print("  → Run: pip install mysqlclient")
    
    # Check app.py configuration
    print_header("5. Production Configuration")
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            content = f.read()
            has_production_config = "os.environ.get('PRODUCTION')" in content
            all_checks_passed &= print_check("Production config in app.py", has_production_config)
            
            has_socketio_threading = "async_mode='threading'" in content
            all_checks_passed &= print_check("Socket.IO threading mode", has_socketio_threading)
            
            has_network_access = "host='0.0.0.0'" in content
            all_checks_passed &= print_check("Network access enabled", has_network_access)
    except Exception as e:
        all_checks_passed &= print_check("app.py readable", False)
        print(f"  Error: {e}")
    
    # Check documentation
    print_header("6. Deployment Documentation")
    docs = [
        "DEPLOY_NOW.md",
        "PYTHONANYWHERE_DEPLOYMENT.md",
        "README_DEPLOYMENT.md",
        "START_HERE.md"
    ]
    for doc in docs:
        print_check(f"{doc}", check_file_exists(doc))
    
    # Final summary
    print_header("VERIFICATION SUMMARY")
    
    if all_checks_passed:
        print("\n🎉 ALL CHECKS PASSED! 🎉")
        print("\nYour LearnLoop application is READY FOR DEPLOYMENT!")
        print("\nNext Steps:")
        print("  1. Test locally: python app.py")
        print("  2. Deploy to PythonAnywhere: Open DEPLOY_NOW.md")
        print("  3. Follow the step-by-step guide")
        print("\n✅ Status: READY TO DEPLOY")
    else:
        print("\n⚠️  SOME CHECKS FAILED")
        print("\nPlease fix the issues marked with ❌ above.")
        print("Then run this script again to verify.")
        print("\n❌ Status: NOT READY - Fix issues first")
    
    print("\n" + "="*70 + "\n")
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    sys.exit(main())

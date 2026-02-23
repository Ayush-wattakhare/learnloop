from flask import Flask, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'learnloop_invertis_2024'

# Database Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'learnloop'

mysql = MySQL(app)

# Test the dashboard query
with app.app_context():
    try:
        cur = mysql.connection.cursor()
        
        # Test query 1: My groups (using a test user_id)
        print("Testing groups query...")
        cur.execute("""SELECT g.* FROM groups g
                       JOIN group_members gm ON g.id = gm.group_id
                       WHERE gm.user_id = %s""", [1])
        my_groups = cur.fetchall()
        print(f"✓ Groups query successful: {len(my_groups)} groups found")
        
        # Test query 2: Suggested partners
        print("\nTesting suggestions query...")
        cur.execute("""SELECT id, name, college, semester, bio FROM users
                       WHERE semester=%s AND id != %s LIMIT 6""", [3, 1])
        suggestions = cur.fetchall()
        print(f"✓ Suggestions query successful: {len(suggestions)} users found")
        
        # Test query 3: Recent notes
        print("\nTesting notes query...")
        cur.execute("""SELECT n.*, u.name as uploader, g.group_name FROM notes n
                       JOIN users u ON n.uploaded_by = u.id
                       JOIN groups g ON n.group_id = g.id
                       JOIN group_members gm ON g.id = gm.group_id
                       WHERE gm.user_id = %s
                       ORDER BY n.uploaded_at DESC LIMIT 5""", [1])
        recent_notes = cur.fetchall()
        print(f"✓ Notes query successful: {len(recent_notes)} notes found")
        
        print("\n✓ All dashboard queries work! The issue might be:")
        print("  1. No user logged in (session['user_id'] not set)")
        print("  2. User doesn't exist in database")
        print("  3. Check if you're accessing /dashboard without logging in")
        
    except Exception as e:
        print(f"✗ Query failed: {e}")
        import traceback
        traceback.print_exc()

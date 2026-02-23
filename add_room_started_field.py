"""
Migration script to add 'started_at' field to voice_rooms table
This tracks when the host actually starts the session
"""

from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'learnloop'

mysql = MySQL(app)

def run_migration():
    """Add started_at field to voice_rooms table"""
    try:
        cur = mysql.connection.cursor()
        
        # Add started_at column
        cur.execute("""
            ALTER TABLE voice_rooms 
            ADD COLUMN started_at TIMESTAMP NULL AFTER created_at
        """)
        
        # Add host_online column to track host presence
        cur.execute("""
            ALTER TABLE voice_rooms 
            ADD COLUMN host_online BOOLEAN DEFAULT FALSE AFTER started_at
        """)
        
        mysql.connection.commit()
        print("✅ Migration successful!")
        print("   - Added 'started_at' column to voice_rooms")
        print("   - Added 'host_online' column to voice_rooms")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        mysql.connection.rollback()

if __name__ == '__main__':
    with app.app_context():
        run_migration()

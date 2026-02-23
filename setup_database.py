"""
LearnLoop Database Setup Script
Run this to automatically create and configure the database
"""

import MySQLdb
import sys
from getpass import getpass

def setup_database():
    print("=" * 60)
    print("LearnLoop Database Setup")
    print("=" * 60)
    print()
    
    # Get MySQL credentials
    print("Enter MySQL credentials (default: root with no password)")
    host = input("MySQL Host [localhost]: ").strip() or "localhost"
    user = input("MySQL User [root]: ").strip() or "root"
    password = getpass("MySQL Password [press Enter if none]: ")
    
    try:
        # Connect to MySQL server
        print("\n🔄 Connecting to MySQL server...")
        conn = MySQLdb.connect(
            host=host,
            user=user,
            passwd=password
        )
        cursor = conn.cursor()
        print("✅ Connected to MySQL successfully!")
        
        # Create database
        print("\n🔄 Creating 'learnloop' database...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS learnloop")
        print("✅ Database 'learnloop' created!")
        
        # Use the database
        cursor.execute("USE learnloop")
        
        # Create tables
        print("\n🔄 Creating tables...")
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id         INT AUTO_INCREMENT PRIMARY KEY,
                name       VARCHAR(100) NOT NULL,
                email      VARCHAR(100) UNIQUE NOT NULL,
                password   VARCHAR(255) NOT NULL,
                semester   INT NOT NULL,
                college    VARCHAR(150) DEFAULT 'Invertis University',
                bio        TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("  ✅ Users table created")
        
        # Groups table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                id          INT AUTO_INCREMENT PRIMARY KEY,
                group_name  VARCHAR(100) NOT NULL,
                subject     VARCHAR(100) NOT NULL,
                semester    INT NOT NULL,
                description TEXT,
                created_by  INT,
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        """)
        print("  ✅ Groups table created")
        
        # Group members table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS group_members (
                id        INT AUTO_INCREMENT PRIMARY KEY,
                group_id  INT,
                user_id   INT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (group_id) REFERENCES groups(id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE KEY unique_member (group_id, user_id)
            )
        """)
        print("  ✅ Group_members table created")
        
        # Notes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id          INT AUTO_INCREMENT PRIMARY KEY,
                group_id    INT,
                uploaded_by INT,
                title       VARCHAR(200),
                file_name   VARCHAR(255),
                file_path   VARCHAR(255),
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (group_id)    REFERENCES groups(id),
                FOREIGN KEY (uploaded_by) REFERENCES users(id)
            )
        """)
        print("  ✅ Notes table created")
        
        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id       INT AUTO_INCREMENT PRIMARY KEY,
                group_id INT,
                user_id  INT,
                message  TEXT NOT NULL,
                sent_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (group_id) REFERENCES groups(id),
                FOREIGN KEY (user_id)  REFERENCES users(id)
            )
        """)
        print("  ✅ Messages table created")
        
        conn.commit()
        
        # Verify tables
        print("\n🔄 Verifying database structure...")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"✅ Found {len(tables)} tables:")
        for table in tables:
            print(f"   - {table[0]}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ DATABASE SETUP COMPLETE!")
        print("=" * 60)
        print("\n📝 Database Configuration:")
        print(f"   Host: {host}")
        print(f"   User: {user}")
        print(f"   Database: learnloop")
        print(f"   Tables: {len(tables)}")
        print("\n🚀 You can now run: python app.py")
        print("=" * 60)
        
        return True
        
    except MySQLdb.Error as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure MySQL/XAMPP is running")
        print("   2. Check your MySQL credentials")
        print("   3. Verify MySQL service is started")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)

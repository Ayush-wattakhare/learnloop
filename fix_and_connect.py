"""
Fix MySQL connection and setup database
Tries multiple connection methods
"""

import MySQLdb
import sys

def try_connection(host, user, password):
    """Try to connect with given credentials"""
    try:
        conn = MySQLdb.connect(
            host=host,
            user=user,
            passwd=password
        )
        return conn
    except:
        return None

def setup_complete_database():
    print("=" * 70)
    print("  LearnLoop Database Connection & Setup")
    print("=" * 70)
    
    # Try different credential combinations
    credentials = [
        ('localhost', 'root', ''),
        ('127.0.0.1', 'root', ''),
        ('localhost', 'root', 'root'),
        ('127.0.0.1', 'root', 'root'),
    ]
    
    conn = None
    working_creds = None
    
    print("\n🔍 Testing MySQL connections...")
    for host, user, password in credentials:
        print(f"   Trying {user}@{host}...", end=" ")
        conn = try_connection(host, user, password)
        if conn:
            print("✅ SUCCESS!")
            working_creds = (host, user, password)
            break
        else:
            print("❌ Failed")
    
    if not conn:
        print("\n❌ Could not connect to MySQL with any credentials!")
        print("\n💡 Please check:")
        print("   1. XAMPP MySQL is running (green in control panel)")
        print("   2. Port 3306 is not blocked")
        print("   3. Try setting MySQL root password in XAMPP")
        return False
    
    try:
        cursor = conn.cursor()
        host, user, password = working_creds
        
        print(f"\n✅ Connected successfully!")
        print(f"   Host: {host}")
        print(f"   User: {user}")
        
        # Drop and create fresh database
        print("\n🔄 Setting up database...")
        cursor.execute("DROP DATABASE IF EXISTS learnloop")
        cursor.execute("CREATE DATABASE learnloop")
        cursor.execute("USE learnloop")
        print("✅ Database 'learnloop' created")
        
        # Create all tables
        print("\n🔄 Creating tables...")
        
        tables_sql = [
            ("users", """
                CREATE TABLE `users` (
                    id         INT AUTO_INCREMENT PRIMARY KEY,
                    name       VARCHAR(100) NOT NULL,
                    email      VARCHAR(100) UNIQUE NOT NULL,
                    password   VARCHAR(255) NOT NULL,
                    semester   INT NOT NULL,
                    college    VARCHAR(150) DEFAULT 'Invertis University',
                    bio        TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """),
            ("groups", """
                CREATE TABLE `groups` (
                    id          INT AUTO_INCREMENT PRIMARY KEY,
                    group_name  VARCHAR(100) NOT NULL,
                    subject     VARCHAR(100) NOT NULL,
                    semester    INT NOT NULL,
                    description TEXT,
                    created_by  INT,
                    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES `users`(id)
                )
            """),
            ("group_members", """
                CREATE TABLE `group_members` (
                    id        INT AUTO_INCREMENT PRIMARY KEY,
                    group_id  INT,
                    user_id   INT,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (group_id) REFERENCES `groups`(id),
                    FOREIGN KEY (user_id) REFERENCES `users`(id),
                    UNIQUE KEY unique_member (group_id, user_id)
                )
            """),
            ("notes", """
                CREATE TABLE `notes` (
                    id          INT AUTO_INCREMENT PRIMARY KEY,
                    group_id    INT,
                    uploaded_by INT,
                    title       VARCHAR(200),
                    file_name   VARCHAR(255),
                    file_path   VARCHAR(255),
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (group_id)    REFERENCES `groups`(id),
                    FOREIGN KEY (uploaded_by) REFERENCES `users`(id)
                )
            """),
            ("messages", """
                CREATE TABLE `messages` (
                    id       INT AUTO_INCREMENT PRIMARY KEY,
                    group_id INT,
                    user_id  INT,
                    message  TEXT NOT NULL,
                    sent_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (group_id) REFERENCES `groups`(id),
                    FOREIGN KEY (user_id)  REFERENCES `users`(id)
                )
            """)
        ]
        
        for table_name, sql in tables_sql:
            cursor.execute(sql)
            print(f"   ✅ {table_name}")
        
        conn.commit()
        
        # Verify
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"\n✅ All {len(tables)} tables created successfully!")
        
        # Update app.py if needed
        if host == '127.0.0.1' or password != '':
            print(f"\n⚠️  NOTE: Update app.py with these credentials:")
            print(f"   MYSQL_HOST = '{host}'")
            print(f"   MYSQL_USER = '{user}'")
            if password:
                print(f"   MYSQL_PASSWORD = '{password}'")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 70)
        print("  ✅ DATABASE READY!")
        print("=" * 70)
        print("\n🚀 Next step: python app.py")
        print("   Then visit: http://127.0.0.1:5000")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        return False

if __name__ == "__main__":
    success = setup_complete_database()
    sys.exit(0 if success else 1)

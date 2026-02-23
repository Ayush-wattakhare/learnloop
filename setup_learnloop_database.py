"""
Setup LearnLoop Database
Creates the learnloop database and all required tables
"""
import MySQLdb

print("=" * 60)
print("  LearnLoop Database Setup")
print("=" * 60)
print()

try:
    # Connect to MySQL (without database)
    print("🔄 Connecting to MySQL...")
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="root"
    )
    cur = db.cursor()
    print("✅ Connected to MySQL")
    print()
    
    # Create database
    print("🔄 Creating learnloop database...")
    cur.execute("CREATE DATABASE IF NOT EXISTS learnloop")
    print("✅ Database 'learnloop' created")
    print()
    
    # Use the database
    cur.execute("USE learnloop")
    
    # Create tables
    print("🔄 Creating tables...")
    
    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            semester INT NOT NULL,
            college VARCHAR(150) DEFAULT 'Invertis University',
            bio TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            profile_picture VARCHAR(255) DEFAULT NULL
        )
    """)
    print("  ✅ users table")
    
    # Groups table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS `groups` (
            id INT AUTO_INCREMENT PRIMARY KEY,
            group_name VARCHAR(100) NOT NULL,
            subject VARCHAR(100) NOT NULL,
            semester INT NOT NULL,
            description TEXT,
            created_by INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_public BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    """)
    print("  ✅ groups table")
    
    # Group members table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS group_members (
            id INT AUTO_INCREMENT PRIMARY KEY,
            group_id INT,
            user_id INT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_id) REFERENCES `groups`(id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE KEY unique_member (group_id, user_id)
        )
    """)
    print("  ✅ group_members table")
    
    # Messages table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            group_id INT,
            user_id INT,
            message TEXT NOT NULL,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_id) REFERENCES `groups`(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    print("  ✅ messages table")
    
    # Notes table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            group_id INT,
            uploaded_by INT,
            title VARCHAR(200),
            file_name VARCHAR(255),
            file_path VARCHAR(255),
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_id) REFERENCES `groups`(id),
            FOREIGN KEY (uploaded_by) REFERENCES users(id)
        )
    """)
    print("  ✅ notes table")
    
    # Voice rooms table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS voice_rooms (
            id INT AUTO_INCREMENT PRIMARY KEY,
            room_name VARCHAR(100) NOT NULL,
            subject VARCHAR(100) NOT NULL,
            description TEXT,
            host_id INT,
            group_id INT,
            is_public BOOLEAN DEFAULT TRUE,
            room_type ENUM('video', 'audio') DEFAULT 'video',
            is_active BOOLEAN DEFAULT TRUE,
            max_stage INT DEFAULT 6,
            room_code VARCHAR(8) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ended_at TIMESTAMP NULL,
            started_at TIMESTAMP NULL,
            host_online BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (host_id) REFERENCES users(id),
            FOREIGN KEY (group_id) REFERENCES `groups`(id)
        )
    """)
    print("  ✅ voice_rooms table")
    
    # Room participants table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS room_participants (
            id INT AUTO_INCREMENT PRIMARY KEY,
            room_id INT,
            user_id INT,
            role ENUM('host', 'moderator', 'stage', 'visitor') DEFAULT 'visitor',
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (room_id) REFERENCES voice_rooms(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    print("  ✅ room_participants table")
    
    # Room messages table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS room_messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            room_id INT,
            user_id INT,
            message TEXT NOT NULL,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (room_id) REFERENCES voice_rooms(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    print("  ✅ room_messages table")
    
    # Whiteboard snapshots table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS whiteboard_snapshots (
            id INT AUTO_INCREMENT PRIMARY KEY,
            room_id INT,
            snapshot_data LONGTEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (room_id) REFERENCES voice_rooms(id)
        )
    """)
    print("  ✅ whiteboard_snapshots table")
    
    # Stage requests table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stage_requests (
            id INT AUTO_INCREMENT PRIMARY KEY,
            room_id INT,
            user_id INT,
            status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (room_id) REFERENCES voice_rooms(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    print("  ✅ stage_requests table")
    
    # Friendships table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS friendships (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            friend_id INT NOT NULL,
            status ENUM('pending', 'accepted', 'rejected') DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (friend_id) REFERENCES users(id),
            UNIQUE KEY unique_friendship (user_id, friend_id)
        )
    """)
    print("  ✅ friendships table")
    
    # Direct messages table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS direct_messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sender_id INT NOT NULL,
            receiver_id INT NOT NULL,
            message TEXT,
            file_name VARCHAR(255),
            file_path VARCHAR(255),
            file_type ENUM('document', 'image', 'pdf', 'other') DEFAULT 'other',
            is_read BOOLEAN DEFAULT FALSE,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id)
        )
    """)
    print("  ✅ direct_messages table")
    
    # Notifications table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            type ENUM('group_created', 'friend_request', 'message', 'group_invite') DEFAULT 'group_created',
            title VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            link VARCHAR(255),
            is_read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    print("  ✅ notifications table")
    
    db.commit()
    
    # Verify tables
    print()
    print("🔄 Verifying tables...")
    cur.execute("SHOW TABLES")
    tables = cur.fetchall()
    
    print(f"✅ {len(tables)} tables created:")
    for table in tables:
        cur.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cur.fetchone()[0]
        print(f"   - {table[0]}: {count} records")
    
    cur.close()
    db.close()
    
    print()
    print("=" * 60)
    print("  ✅ LearnLoop Database Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Run: python app.py")
    print("2. Open: http://127.0.0.1:5000")
    print("3. Register and start using LearnLoop!")
    print()
    
except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("Troubleshooting:")
    print("1. Make sure MySQL is running (XAMPP)")
    print("2. Check MySQL credentials (root/root)")
    print("3. Try running XAMPP as administrator")

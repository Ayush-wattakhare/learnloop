"""
Setup Voice Rooms Feature
Installs dependencies and creates database tables
"""

import subprocess
import sys
import MySQLdb

def install_dependencies():
    """Install required packages"""
    print("=" * 70)
    print("  Installing Voice Room Dependencies")
    print("=" * 70)
    print()
    
    packages = ['flask-socketio', 'python-socketio', 'eventlet']
    
    for package in packages:
        print(f"📦 Installing {package}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    print("\n✅ All dependencies installed!")
    return True

def setup_database():
    """Create voice room tables"""
    print("\n" + "=" * 70)
    print("  Setting Up Voice Room Database Tables")
    print("=" * 70)
    print()
    
    try:
        # Connect to database
        print("🔄 Connecting to database...")
        conn = MySQLdb.connect(
            host='localhost',
            user='root',
            passwd='root',
            db='learnloop'
        )
        cursor = conn.cursor()
        print("✅ Connected to database")
        
        # Create tables
        tables = [
            ("voice_rooms", """
                CREATE TABLE IF NOT EXISTS `voice_rooms` (
                    id          INT AUTO_INCREMENT PRIMARY KEY,
                    room_name   VARCHAR(150) NOT NULL,
                    subject     VARCHAR(100) NOT NULL,
                    description TEXT,
                    host_id     INT NOT NULL,
                    group_id    INT NULL,
                    is_public   BOOLEAN DEFAULT TRUE,
                    is_active   BOOLEAN DEFAULT TRUE,
                    max_stage   INT DEFAULT 6,
                    room_code   VARCHAR(20) UNIQUE NOT NULL,
                    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ended_at    TIMESTAMP NULL,
                    FOREIGN KEY (host_id) REFERENCES `users`(id),
                    FOREIGN KEY (group_id) REFERENCES `groups`(id)
                )
            """),
            ("room_participants", """
                CREATE TABLE IF NOT EXISTS `room_participants` (
                    id          INT AUTO_INCREMENT PRIMARY KEY,
                    room_id     INT NOT NULL,
                    user_id     INT NOT NULL,
                    role        ENUM('host', 'stage', 'audience') DEFAULT 'audience',
                    is_video_on BOOLEAN DEFAULT FALSE,
                    is_audio_on BOOLEAN DEFAULT FALSE,
                    joined_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    left_at     TIMESTAMP NULL,
                    FOREIGN KEY (room_id) REFERENCES `voice_rooms`(id),
                    FOREIGN KEY (user_id) REFERENCES `users`(id)
                )
            """),
            ("room_messages", """
                CREATE TABLE IF NOT EXISTS `room_messages` (
                    id         INT AUTO_INCREMENT PRIMARY KEY,
                    room_id    INT NOT NULL,
                    user_id    INT NOT NULL,
                    message    TEXT NOT NULL,
                    is_pinned  BOOLEAN DEFAULT FALSE,
                    sent_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (room_id) REFERENCES `voice_rooms`(id),
                    FOREIGN KEY (user_id) REFERENCES `users`(id)
                )
            """),
            ("stage_requests", """
                CREATE TABLE IF NOT EXISTS `stage_requests` (
                    id          INT AUTO_INCREMENT PRIMARY KEY,
                    room_id     INT NOT NULL,
                    user_id     INT NOT NULL,
                    status      ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
                    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    responded_at TIMESTAMP NULL,
                    FOREIGN KEY (room_id) REFERENCES `voice_rooms`(id),
                    FOREIGN KEY (user_id) REFERENCES `users`(id)
                )
            """),
            ("whiteboard_snapshots", """
                CREATE TABLE IF NOT EXISTS `whiteboard_snapshots` (
                    id          INT AUTO_INCREMENT PRIMARY KEY,
                    room_id     INT NOT NULL,
                    snapshot_data LONGTEXT NOT NULL,
                    created_by  INT NOT NULL,
                    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (room_id) REFERENCES `voice_rooms`(id),
                    FOREIGN KEY (created_by) REFERENCES `users`(id)
                )
            """)
        ]
        
        print("\n🔄 Creating tables...")
        for table_name, sql in tables:
            cursor.execute(sql)
            print(f"   ✅ {table_name}")
        
        # Create indexes
        print("\n🔄 Creating indexes...")
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_voice_rooms_active ON `voice_rooms`(is_active)",
            "CREATE INDEX IF NOT EXISTS idx_voice_rooms_host ON `voice_rooms`(host_id)",
            "CREATE INDEX IF NOT EXISTS idx_room_participants_room ON `room_participants`(room_id)",
            "CREATE INDEX IF NOT EXISTS idx_room_participants_user ON `room_participants`(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_room_messages_room ON `room_messages`(room_id)",
            "CREATE INDEX IF NOT EXISTS idx_stage_requests_room ON `stage_requests`(room_id)"
        ]
        
        for index_sql in indexes:
            try:
                cursor.execute(index_sql)
            except:
                pass  # Index might already exist
        
        print("   ✅ Indexes created")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✅ Database tables created successfully!")
        return True
        
    except MySQLdb.Error as e:
        print(f"\n❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    print("\n" + "=" * 70)
    print("  LearnLoop Voice Rooms Feature Setup")
    print("=" * 70)
    print()
    print("This will:")
    print("  1. Install required Python packages")
    print("  2. Create voice room database tables")
    print("  3. Set up indexes for performance")
    print()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation")
        return False
    
    # Setup database
    if not setup_database():
        print("\n❌ Setup failed at database creation")
        return False
    
    print("\n" + "=" * 70)
    print("  ✅ VOICE ROOMS FEATURE READY!")
    print("=" * 70)
    print()
    print("🎉 Setup complete! You can now:")
    print("   1. Start the application: python app.py")
    print("   2. Navigate to Voice Rooms in the menu")
    print("   3. Create your first voice room")
    print()
    print("📝 Features available:")
    print("   ✅ Live video calls (up to 6 on stage)")
    print("   ✅ Shared whiteboard")
    print("   ✅ Real-time chat")
    print("   ✅ Screen sharing")
    print("   ✅ Unlimited audience")
    print()
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

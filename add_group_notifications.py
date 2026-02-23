import MySQLdb

# Database connection
db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="root",
    db="learnloop"
)

cur = db.cursor()

try:
    # Create notifications table
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
    print("✅ Created notifications table")
    
    # Add is_public column to groups if not exists
    cur.execute("DESCRIBE `groups`")
    columns = [col[0] for col in cur.fetchall()]
    
    if 'is_public' not in columns:
        cur.execute("""
            ALTER TABLE `groups` 
            ADD COLUMN is_public BOOLEAN DEFAULT TRUE
        """)
        print("✅ Added is_public column to groups table")
    else:
        print("✓ is_public column already exists")
    
    # Update existing groups to be public
    cur.execute("UPDATE `groups` SET is_public = TRUE WHERE is_public IS NULL")
    print("✅ Updated existing groups to public")
    
    db.commit()
    print("\n✅ Notification system setup complete!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()

cur.close()
db.close()

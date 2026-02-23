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
    print("✅ Created friendships table")
    
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
    print("✅ Created direct_messages table")
    
    db.commit()
    print("✅ All messaging tables created successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()

cur.close()
db.close()

import MySQLdb

try:
    conn = MySQLdb.connect(
        host='localhost',
        user='root',
        password='root',
        database='learnloop'
    )
    
    cur = conn.cursor()
    
    # Add room_type column
    cur.execute("ALTER TABLE voice_rooms ADD COLUMN room_type ENUM('video', 'audio') DEFAULT 'video' AFTER is_public")
    conn.commit()
    
    print("✓ Database updated successfully!")
    print("  - Added room_type column to voice_rooms table")
    
    conn.close()
    
except MySQLdb.Error as e:
    if "Duplicate column name" in str(e):
        print("✓ Column already exists, skipping...")
    else:
        print(f"✗ Error: {e}")

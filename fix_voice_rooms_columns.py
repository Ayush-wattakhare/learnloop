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
    # Check if columns exist
    cur.execute("DESCRIBE voice_rooms")
    columns = [col[0] for col in cur.fetchall()]
    
    # Add started_at if missing
    if 'started_at' not in columns:
        cur.execute("""
            ALTER TABLE voice_rooms 
            ADD COLUMN started_at TIMESTAMP NULL DEFAULT NULL
        """)
        print("✅ Added started_at column")
    else:
        print("✓ started_at column already exists")
    
    # Add host_online if missing
    if 'host_online' not in columns:
        cur.execute("""
            ALTER TABLE voice_rooms 
            ADD COLUMN host_online BOOLEAN DEFAULT FALSE
        """)
        print("✅ Added host_online column")
    else:
        print("✓ host_online column already exists")
    
    # Add is_live if missing (alias for is_active)
    if 'is_live' not in columns and 'is_active' in columns:
        print("✓ Using is_active as is_live")
    
    db.commit()
    print("\n✅ Voice rooms table updated successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()

cur.close()
db.close()

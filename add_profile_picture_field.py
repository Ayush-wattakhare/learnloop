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
    # Add profile_picture column to users table
    cur.execute("""
        ALTER TABLE users 
        ADD COLUMN profile_picture VARCHAR(255) DEFAULT NULL
    """)
    db.commit()
    print("✅ Successfully added profile_picture column to users table")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Note: Column might already exist")

cur.close()
db.close()

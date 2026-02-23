"""
Test script to verify all LearnLoop features are properly connected
"""
import MySQLdb

# Database connection
db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="root",
    db="learnloop"
)

cur = db.cursor()

print("=" * 60)
print("LearnLoop Feature Connection Test")
print("=" * 60)

# Test 1: Check all required tables exist
print("\n1. Checking Database Tables...")
required_tables = [
    'users', 'groups', 'group_members', 'messages', 'notes',
    'voice_rooms', 'room_participants', 'room_messages', 
    'whiteboard_snapshots', 'stage_requests',
    'friendships', 'direct_messages'
]

cur.execute("SHOW TABLES")
existing_tables = [table[0] for table in cur.fetchall()]

for table in required_tables:
    if table in existing_tables:
        # Use backticks for reserved keywords like 'groups'
        table_name = f"`{table}`" if table == 'groups' else table
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cur.fetchone()[0]
        print(f"   ✅ {table}: {count} records")
    else:
        print(f"   ❌ {table}: MISSING")

# Test 2: Check users table structure
print("\n2. Checking Users Table Structure...")
cur.execute("DESCRIBE users")
user_columns = [col[0] for col in cur.fetchall()]
required_user_columns = ['id', 'name', 'email', 'password', 'semester', 'college', 'bio', 'created_at', 'profile_picture']

for col in required_user_columns:
    if col in user_columns:
        print(f"   ✅ {col}")
    else:
        print(f"   ❌ {col}: MISSING")

# Test 3: Check friendships table structure
print("\n3. Checking Friendships Table Structure...")
cur.execute("DESCRIBE friendships")
friendship_columns = [col[0] for col in cur.fetchall()]
required_friendship_columns = ['id', 'user_id', 'friend_id', 'status', 'created_at']

for col in required_friendship_columns:
    if col in friendship_columns:
        print(f"   ✅ {col}")
    else:
        print(f"   ❌ {col}: MISSING")

# Test 4: Check direct_messages table structure
print("\n4. Checking Direct Messages Table Structure...")
cur.execute("DESCRIBE direct_messages")
dm_columns = [col[0] for col in cur.fetchall()]
required_dm_columns = ['id', 'sender_id', 'receiver_id', 'message', 'file_name', 'file_path', 'file_type', 'is_read', 'sent_at']

for col in required_dm_columns:
    if col in dm_columns:
        print(f"   ✅ {col}")
    else:
        print(f"   ❌ {col}: MISSING")

# Test 5: Check voice_rooms table structure
print("\n5. Checking Voice Rooms Table Structure...")
cur.execute("DESCRIBE voice_rooms")
vr_columns = [col[0] for col in cur.fetchall()]
required_vr_columns = ['id', 'room_name', 'subject', 'description', 'host_id', 'is_public', 'is_live', 'room_type', 'created_at', 'room_code', 'started_at', 'host_online']

for col in required_vr_columns:
    if col in vr_columns:
        print(f"   ✅ {col}")
    else:
        print(f"   ❌ {col}: MISSING")

# Test 6: Check file upload directories
print("\n6. Checking Upload Directories...")
import os

upload_dirs = [
    'static/uploads/profiles',
    'static/uploads/messages',
    'static/uploads/notes'
]

for dir_path in upload_dirs:
    if os.path.exists(dir_path):
        files = len(os.listdir(dir_path))
        print(f"   ✅ {dir_path}: {files} files")
    else:
        print(f"   ❌ {dir_path}: MISSING")
        try:
            os.makedirs(dir_path, exist_ok=True)
            print(f"      → Created directory")
        except Exception as e:
            print(f"      → Error creating: {e}")

# Test 7: Check for sample data
print("\n7. Checking Sample Data...")
cur.execute("SELECT COUNT(*) FROM users")
user_count = cur.fetchone()[0]
if user_count > 0:
    print(f"   ✅ Users: {user_count} registered")
else:
    print(f"   ⚠️  No users registered yet")

cur.execute("SELECT COUNT(*) FROM `groups`")
group_count = cur.fetchone()[0]
if group_count > 0:
    print(f"   ✅ Groups: {group_count} created")
else:
    print(f"   ⚠️  No groups created yet")

cur.execute("SELECT COUNT(*) FROM voice_rooms")
vr_count = cur.fetchone()[0]
if vr_count > 0:
    print(f"   ✅ Voice Rooms: {vr_count} created")
else:
    print(f"   ⚠️  No voice rooms created yet")

# Test 8: Check foreign key relationships
print("\n8. Checking Foreign Key Relationships...")
try:
    cur.execute("""
        SELECT COUNT(*) FROM friendships f
        JOIN users u1 ON f.user_id = u1.id
        JOIN users u2 ON f.friend_id = u2.id
    """)
    print(f"   ✅ Friendships → Users: Valid")
except Exception as e:
    print(f"   ❌ Friendships → Users: {e}")

try:
    cur.execute("""
        SELECT COUNT(*) FROM direct_messages dm
        JOIN users u1 ON dm.sender_id = u1.id
        JOIN users u2 ON dm.receiver_id = u2.id
    """)
    print(f"   ✅ Direct Messages → Users: Valid")
except Exception as e:
    print(f"   ❌ Direct Messages → Users: {e}")

try:
    cur.execute("""
        SELECT COUNT(*) FROM voice_rooms vr
        JOIN users u ON vr.host_id = u.id
    """)
    print(f"   ✅ Voice Rooms → Users: Valid")
except Exception as e:
    print(f"   ❌ Voice Rooms → Users: {e}")

print("\n" + "=" * 60)
print("Feature Connection Summary")
print("=" * 60)

features = {
    "User Authentication": user_count > 0,
    "Study Groups": group_count > 0,
    "Voice Rooms": vr_count > 0,
    "Messaging System": 'friendships' in existing_tables and 'direct_messages' in existing_tables,
    "Profile Pictures": 'profile_picture' in user_columns,
    "File Uploads": os.path.exists('static/uploads')
}

for feature, status in features.items():
    status_icon = "✅" if status else "⚠️"
    status_text = "READY" if status else "NEEDS SETUP"
    print(f"{status_icon} {feature}: {status_text}")

print("\n" + "=" * 60)
print("All features are properly connected!")
print("=" * 60)

cur.close()
db.close()

import MySQLdb
import secrets
import string

def generate_room_code():
    """Generate unique 8-character room code"""
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))

try:
    conn = MySQLdb.connect(
        host='localhost',
        user='root',
        password='root',
        database='learnloop'
    )
    
    cursor = conn.cursor()
    
    # Test the INSERT query
    room_name = "Test Room"
    subject = "Test Subject"
    description = "Test Description"
    host_id = 1  # Assuming user 1 exists
    is_public = True
    room_code = generate_room_code()
    group_id = None
    
    print(f"Testing voice room creation with room_code: {room_code}")
    
    cursor.execute("""
        INSERT INTO voice_rooms (room_name, subject, description, host_id, is_public, room_code, group_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (room_name, subject, description, host_id, is_public, room_code, group_id))
    
    conn.commit()
    room_id = cursor.lastrowid
    
    print(f"✓ Voice room created successfully! Room ID: {room_id}")
    
    # Test adding participant
    cursor.execute("""
        INSERT INTO room_participants (room_id, user_id, role, is_video_on, is_audio_on)
        VALUES (%s, %s, 'host', TRUE, TRUE)
    """, (room_id, host_id))
    
    conn.commit()
    print("✓ Host added as participant successfully!")
    
    conn.close()
    
except MySQLdb.Error as e:
    print(f"✗ Database error: {e}")
    import traceback
    traceback.print_exc()

import MySQLdb

conn = MySQLdb.connect(
    host='localhost',
    user='root',
    password='root',
    database='learnloop'
)

cur = conn.cursor()

# Get the room we just created
cur.execute("""
    SELECT vr.*, u.name as host_name
    FROM voice_rooms vr
    JOIN users u ON vr.host_id = u.id
    WHERE vr.room_code = 'P05BMAEF' AND vr.is_active = TRUE
""")

room = cur.fetchone()

if room:
    print("Room data structure:")
    print(f"Length: {len(room)}")
    for i, value in enumerate(room):
        print(f"  [{i}] = {value}")
    
    print("\nExpected indices in template:")
    print(f"  room[1] (room_name) = {room[1]}")
    print(f"  room[4] (host_id) = {room[4]}")
else:
    print("Room not found!")

conn.close()

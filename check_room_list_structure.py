import MySQLdb

conn = MySQLdb.connect(
    host='localhost',
    user='root',
    password='root',
    database='learnloop'
)

cur = conn.cursor()
cur.execute("""
    SELECT vr.*, u.name as host_name,
           (SELECT COUNT(*) FROM room_participants WHERE room_id=vr.id AND role='stage') as stage_count
    FROM voice_rooms vr
    JOIN users u ON vr.host_id = u.id
    WHERE vr.is_active = TRUE
    LIMIT 1
""")

room = cur.fetchone()

if room:
    print("Room list structure:")
    for i, v in enumerate(room):
        print(f"[{i}] = {v}")
    print(f"\nhost_id is at index [4] = {room[4]}")
    print(f"room_code is at index [10] = {room[10]}")
else:
    print("No active rooms found")

conn.close()

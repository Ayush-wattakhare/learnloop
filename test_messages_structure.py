import MySQLdb

conn = MySQLdb.connect(
    host='localhost',
    user='root',
    password='root',
    database='learnloop'
)

cur = conn.cursor()

# Simulate the messages query
cur.execute("""
    SELECT rm.*, u.name as sender_name
    FROM room_messages rm
    JOIN users u ON rm.user_id = u.id
    WHERE rm.room_id = 1
    ORDER BY rm.sent_at DESC
    LIMIT 50
""")

messages = cur.fetchall()

if messages:
    print("Message data structure:")
    print(f"Length: {len(messages[0])}")
    for i, value in enumerate(messages[0]):
        print(f"  [{i}] = {value}")
    
    print("\nTemplate expects:")
    print("  message[4] = sender_name")
    print("  message[3] = sent_at")
    print("  message[2] = message text")
else:
    print("No messages found (this is OK for a new room)")

conn.close()

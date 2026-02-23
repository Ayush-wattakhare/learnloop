import MySQLdb

try:
    # Test connection with your credentials
    conn = MySQLdb.connect(
        host='localhost',
        user='root',
        password='root',
        database='learnloop'
    )
    print("✓ Database connection successful!")
    
    # Test if tables exist
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    if tables:
        print(f"✓ Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
    else:
        print("⚠ Database exists but no tables found. Run database.sql to create tables.")
    
    conn.close()
    
except MySQLdb.Error as e:
    print(f"✗ Database connection failed: {e}")
    print("\nPossible solutions:")
    print("1. Make sure MySQL server is running")
    print("2. Check if database 'learnloop' exists")
    print("3. Verify username/password are correct")
    print("4. Run: mysql -u root -p < database.sql")

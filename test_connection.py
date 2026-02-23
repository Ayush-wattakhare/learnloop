"""
Test MySQL Connection
Quick script to verify database connectivity
"""

import MySQLdb
import sys

def test_connection():
    print("=" * 60)
    print("Testing MySQL Connection")
    print("=" * 60)
    
    try:
        print("\n🔄 Attempting to connect to MySQL...")
        conn = MySQLdb.connect(
            host='localhost',
            user='root',
            passwd='root',
            db='learnloop'
        )
        
        print("✅ Connection successful!")
        
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()
        print(f"✅ Connected to database: {db_name[0]}")
        
        # Check tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"\n📊 Found {len(tables)} tables:")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
            count = cursor.fetchone()[0]
            print(f"   - {table_name}: {count} records")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ DATABASE IS READY!")
        print("=" * 60)
        print("\n🚀 Run: python app.py")
        
        return True
        
    except MySQLdb.Error as e:
        print(f"\n❌ Connection failed: {e}")
        print("\n💡 Solutions:")
        print("   1. Run: python setup_database.py")
        print("   2. Make sure XAMPP MySQL is running")
        print("   3. Check database credentials in app.py")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)

print("TEST SCRIPT STARTED")

from config.database import get_db_connection


connection = None

try:
    connection = get_db_connection()

    print("SUCCESS: Connected to MySQL!")

    cursor = connection.cursor()

    cursor.execute("SELECT DATABASE()")

    result = cursor.fetchone()

    print("Connected database:", result[0])

    cursor.execute("SELECT COUNT(*) FROM users")

    user_count = cursor.fetchone()[0]

    print("Total users:", user_count)

    cursor.close()

except Exception as error:
    print("DATABASE CONNECTION FAILED")
    print("Error:", error)

finally:
    if connection and connection.is_connected():
        connection.close()
        print("Database connection closed.")

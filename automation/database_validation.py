
"""
PulsePay Product Analytics
Database Validation Module

Checks database connectivity and essential table availability.
Performs read-only operations only.
"""

from config.database import get_db_connection


# ============================================================
# REQUIRED DATABASE TABLES
# ============================================================

REQUIRED_TABLES = [
    "users",
    "kyc_applications",
    "events",
    "transactions",
    "experiment_assignments",
    "support_tickets",
]


# ============================================================
# DATABASE VALIDATION
# ============================================================

def validate_database():

    connection = None

    try:

        print("\n" + "=" * 70)
        print("PULSEPAY DATABASE VALIDATION")
        print("=" * 70)

        # Establish database connection
        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        print("\n[PASS] MySQL connection established.")

        # Identify connected database
        cursor.execute("SELECT DATABASE() AS database_name")

        database_result = cursor.fetchone()

        database_name = database_result["database_name"]

        print(f"[INFO] Connected database: {database_name}")

        # Retrieve available tables
        cursor.execute("""
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = DATABASE()
        """)

        available_tables = {
            row["TABLE_NAME"]
            for row in cursor.fetchall()
        }

        # Check required tables
        missing_tables = []

        for table in REQUIRED_TABLES:

            if table in available_tables:

                print(f"[PASS] Table exists: {table}")

            else:

                print(f"[FAIL] Missing table: {table}")

                missing_tables.append(table)

        cursor.close()

        # Final validation result
        if missing_tables:

            print("\n[FAIL] Database validation unsuccessful.")

            return False

        print("\n[PASS] All required tables are available.")

        return True

    except Exception as error:

        print(f"\n[ERROR] Database validation failed: {error}")

        return False

    finally:

        if connection is not None and connection.is_connected():

            connection.close()

            print("\nDatabase connection closed.")

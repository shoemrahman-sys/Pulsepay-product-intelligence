
"""
PulsePay Product Analytics
Dashboard SQL Automation

Creates the 10 reusable MySQL views required by
the PulsePay Power BI dashboard and results exporter.

Does not generate, reload, insert, update, or delete raw data.
"""

from pathlib import Path

from config.database import get_db_connection


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DASHBOARD_SQL_DIR = PROJECT_ROOT / "sql" / "04_dashboard"


# ============================================================
# SQL FILE EXECUTION ORDER
# ============================================================

SQL_FILES = [
    "001_create_dashboard_views.sql",
    "002_create_incident_impact_view.sql",
]


# ============================================================
# EXPECTED DASHBOARD VIEWS
# ============================================================

EXPECTED_VIEWS = [
    "vw_executive_kpis",
    "vw_weekly_north_star",
    "vw_onboarding_funnel",
    "vw_kyc_device_version",
    "vw_weekly_kyc_trend",
    "vw_acquisition_quality",
    "vw_activation_retention",
    "vw_cohort_retention",
    "vw_experiment_scorecard",
    "vw_kyc_incident_impact",
]


# ============================================================
# SQL FILE EXECUTION
# ============================================================

def execute_sql_file(cursor, sql_file):

    file_path = DASHBOARD_SQL_DIR / sql_file

    if not file_path.exists():
        raise FileNotFoundError(
            f"SQL file not found: {file_path}"
        )

    print(f"\nExecuting SQL file: {sql_file}")

    sql_script = file_path.read_text(encoding="utf-8")

    statements = [
        statement.strip()
        for statement in sql_script.split(";")
        if statement.strip()
    ]

    for statement in statements:
        cursor.execute(statement)

    print(f"[PASS] Completed: {sql_file}")


# ============================================================
# VERIFY CREATED VIEWS
# ============================================================

def verify_dashboard_views(cursor):

    cursor.execute("""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.VIEWS
        WHERE TABLE_SCHEMA = DATABASE()
    """)

    available_views = {
        row[0] for row in cursor.fetchall()
    }

    missing_views = []

    print("\nVerifying dashboard views:\n")

    for view in EXPECTED_VIEWS:

        if view in available_views:
            print(f"[PASS] View exists: {view}")
        else:
            print(f"[FAIL] Missing view: {view}")
            missing_views.append(view)

    if missing_views:
        print("\n[FAIL] Dashboard view verification failed.")
        return False

    print("\n[PASS] All 10 dashboard views are available.")

    return True


# ============================================================
# MAIN DASHBOARD SQL AUTOMATION
# ============================================================

def run_sql_analysis():

    connection = None
    cursor = None

    try:

        print("\n" + "=" * 70)
        print("PULSEPAY DASHBOARD SQL AUTOMATION")
        print("=" * 70)

        connection = get_db_connection()

        cursor = connection.cursor()

        print("\n[PASS] MySQL connection established.")

        cursor.execute("SELECT DATABASE()")
        database_name = cursor.fetchone()[0]

        if database_name != "pulsepay_analytics":
            raise RuntimeError(
                f"Unexpected database: {database_name}"
            )

        print(f"[INFO] Connected database: {database_name}")

        # Execute dashboard view definitions in order.
        for sql_file in SQL_FILES:
            execute_sql_file(cursor, sql_file)

        # Confirm that all required views exist.
        verification_success = verify_dashboard_views(cursor)

        if not verification_success:
            return False

        print("\n[PASS] Dashboard SQL automation completed.")

        return True

    except Exception as error:

        print(
            f"\n[ERROR] Dashboard SQL automation failed: {error}"
        )

        print(
            "[WARNING] Some views may already have been created "
            "or replaced. MySQL DDL changes are not reliably "
            "reversed by rollback."
        )

        return False

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()
            print("\nMySQL connection closed.")

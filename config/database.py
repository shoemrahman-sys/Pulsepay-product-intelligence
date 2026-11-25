
import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv


# Locate the main PulsePay project directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load environment variables
ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(ENV_FILE)


# Central database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "pulsepay_analytics"),
}


def get_db_connection():
    """
    Create and return a MySQL database connection.
    """

    if not DB_CONFIG["password"]:
        raise ValueError(
            "Database password is missing. Check your .env file."
        )

    connection = mysql.connector.connect(**DB_CONFIG)

    return connection

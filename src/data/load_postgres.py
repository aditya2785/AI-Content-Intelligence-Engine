import csv
from getpass import getpass
from pathlib import Path

import psycopg2


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "processed"

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
}


# ---------------------------------------------------------
# Expected CSV columns
# ---------------------------------------------------------

EXPECTED_COLUMNS = {
    "users_clean.csv": [
        "user_id",
        "country",
        "age_group",
        "signup_date",
        "following_count",
        "creator_flag",
        "preferred_genres",
    ],

    "creators_clean.csv": [
        "creator_id",
        "creator_name",
        "signup_date",
        "creator_type",
        "followers",
    ],

    "content_clean.csv": [
        "content_id",
        "creator_id",
        "content_type",
        "genre",
        "created_at",
        "duration",
        "tags",
        "is_template",
        "is_recreation",
    ],

    "interactions_clean.csv": [
        "user_id",
        "content_id",
        "creator_id",
        "genre",
        "content_type",
        "duration",
        "creator_followers",
        "content_created_at",
        "genre_match",
        "timestamp",
        "content_age_days",
        "freshness",
        "impression",
        "clicked",
        "watch_time",
        "completion_rate",
        "liked",
        "saved",
        "shared",
        "commented",
        "recreated",
        "meaningful_engagement",
    ],
}


# ---------------------------------------------------------
# Database connection
# ---------------------------------------------------------

def create_connection():
    password = getpass("PostgreSQL password: ")

    connection = psycopg2.connect(
        **DB_CONFIG,
        password=password,
    )

    return connection


# ---------------------------------------------------------
# Validate CSV structure
# ---------------------------------------------------------

def validate_csv_columns(
    file_path: Path,
    expected_columns: list[str],
) -> None:

    with file_path.open(
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        reader = csv.reader(file)
        actual_columns = next(reader)

    if actual_columns != expected_columns:
        raise ValueError(
            f"\nColumn mismatch in {file_path.name}\n\n"
            f"Expected:\n{expected_columns}\n\n"
            f"Found:\n{actual_columns}"
        )

    print(f"✓ Columns validated: {file_path.name}")


# ---------------------------------------------------------
# Load a CSV using PostgreSQL COPY
# ---------------------------------------------------------

def load_csv(
    cursor,
    file_path: Path,
    table_name: str,
    columns: list[str],
) -> None:

    column_sql = ", ".join(
        f'"{column}"'
        for column in columns
    )

    copy_sql = f"""
        COPY {table_name} ({column_sql})
        FROM STDIN
        WITH (
            FORMAT CSV,
            HEADER TRUE,
            DELIMITER ',',
            QUOTE '"'
        )
    """

    with file_path.open(
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        cursor.copy_expert(
            copy_sql,
            file
        )

    print(
        f"✓ Loaded {file_path.name} → {table_name}"
    )


# ---------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("AICines Content Intelligence")
    print("PostgreSQL Data Loader")
    print("=" * 60)

    files = {
        "users_clean.csv": "users",
        "creators_clean.csv": "creators",
        "content_clean.csv": "content",
        "interactions_clean.csv": "interactions",
    }

    # Check files exist
    for filename in files:
        file_path = DATA_PATH / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

    # Validate CSV structures before touching database
    print("\nValidating CSV files...")

    for filename, columns in EXPECTED_COLUMNS.items():
        validate_csv_columns(
            DATA_PATH / filename,
            columns
        )

    print("\nConnecting to PostgreSQL...")

    connection = create_connection()

    try:
        cursor = connection.cursor()

        print("✓ Connected successfully.")

        # Clear existing data
        print("\nClearing existing tables...")

        cursor.execute("""
            TRUNCATE TABLE
                interactions,
                content,
                creators,
                users
            RESTART IDENTITY
            CASCADE;
        """)

        # Load in dependency order
        load_csv(
            cursor,
            DATA_PATH / "users_clean.csv",
            "users",
            EXPECTED_COLUMNS["users_clean.csv"],
        )

        load_csv(
            cursor,
            DATA_PATH / "creators_clean.csv",
            "creators",
            EXPECTED_COLUMNS["creators_clean.csv"],
        )

        load_csv(
            cursor,
            DATA_PATH / "content_clean.csv",
            "content",
            EXPECTED_COLUMNS["content_clean.csv"],
        )

        load_csv(
            cursor,
            DATA_PATH / "interactions_clean.csv",
            "interactions",
            EXPECTED_COLUMNS["interactions_clean.csv"],
        )

        connection.commit()

        print("\n" + "=" * 60)
        print("DATA LOAD COMPLETED SUCCESSFULLY")
        print("=" * 60)

        # Verify row counts
        print("\nDatabase row counts:")

        for table in files.values():

            cursor.execute(
                f"SELECT COUNT(*) FROM {table};"
            )

            count = cursor.fetchone()[0]

            print(
                f"{table:<15} {count:>10,}"
            )

        cursor.close()

    except Exception:
        connection.rollback()
        print("\n❌ ERROR: Transaction rolled back.")
        raise

    finally:
        connection.close()
        print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()
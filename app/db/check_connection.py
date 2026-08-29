import sys

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import engine


def check_database_connection() -> None:
    """Open a database connection and execute a minimal PostgreSQL query."""

    try:
        with engine.connect() as connection:
            result = connection.execute(
                text(
                    """
                    SELECT
                        current_database() AS database_name,
                        current_user AS database_user,
                        version() AS database_version
                    """
                )
            ).mappings().one()

        print("Database connection successful.")
        print(f"Database: {result['database_name']}")
        print(f"User: {result['database_user']}")
        print(f"Version: {result['database_version']}")

    except SQLAlchemyError as exc:
        print("Database connection failed.", file=sys.stderr)
        print(f"Error type: {type(exc).__name__}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    check_database_connection()
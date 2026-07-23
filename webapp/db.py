import os
from pathlib import Path

import psycopg

DATABASE_URL = os.environ["DATABASE_URL"]
PASSWORD_FILE = Path(__file__).resolve().parent.parent / "data" / "100k-most-used-passwords-NCSC.txt"


def connect():
    return psycopg.connect(DATABASE_URL)


def init_database():
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS common_passwords (password TEXT NOT NULL)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS common_passwords_password_idx "
                "ON common_passwords (password)"
            )
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS "2400857" '
                "(id BIGSERIAL PRIMARY KEY, username VARCHAR(100) NOT NULL, "
                "creation_time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP)"
            )
            cursor.execute("SELECT COUNT(*) FROM common_passwords")
            if cursor.fetchone()[0] == 0:
                with cursor.copy("COPY common_passwords (password) FROM STDIN") as copy:
                    for password in PASSWORD_FILE.read_text(
                        encoding="utf-8"
                    ).splitlines():
                        if password:
                            copy.write_row((password,))


def is_common_password(password):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT EXISTS (SELECT 1 FROM common_passwords "
                "WHERE password = %s LIMIT 1)",
                (password,),
            )
            return cursor.fetchone()[0]


def log_account_creation(username):
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO "2400857" (username) VALUES (%s)',
                (username,),
            )


if __name__ == "__main__":
    init_database()

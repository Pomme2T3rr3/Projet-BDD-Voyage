import psycopg2  # type: ignore
import psycopg2.extras  # type: ignore


def connect():
    conn = psycopg2.connect(
        dbname="projet-voyage", cursor_factory=psycopg2.extras.NamedTupleCursor
    )
    conn.autocommit = True
    return conn

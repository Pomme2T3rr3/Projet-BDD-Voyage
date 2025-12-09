import psycopg2  # type: ignore
import psycopg2.extras  # type: ignore


def connect():
    conn = psycopg2.connect(
        dbname="voyage", cursor_factory=psycopg2.extras.NamedTupleCursor
    )
    conn.autocommit = True
    return conn

def connect2():
    conn = psycopg2.connect(
        host = "sqledu.univ-eiffel.fr",
        dbname = "ntelombila.matingou_db",
        password = "NTeloMbila.mtg77", # MDP de la connexion à BDD de la fac 
        cursor_factory = psycopg2.extras.NamedTupleCursor
    )
    conn.autocommit = True
    return conn
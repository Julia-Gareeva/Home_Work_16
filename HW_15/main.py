import sqlite3
from querys import DATABASE_SOURCE, CREATE_QUERIES, MIGRATE_SECOND, MIGRATE_JOIN


def get_sqlite_query(query, base=DATABASE_SOURCE, is_script=False):
    with sqlite3.connect(base) as connection:
        cursor = connection.cursor()
        if is_script:
            cursor.executescript(query)
        else:
            cursor.execute(query)


get_sqlite_query(CREATE_QUERIES, is_script=True)

get_sqlite_query(MIGRATE_SECOND, is_script=True)

get_sqlite_query(MIGRATE_JOIN, is_script=False)
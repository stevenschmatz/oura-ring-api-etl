"""
load.py

Functions to load data into the database.
"""

from psycopg2 import sql


def upload_row(table_name, row_dict, connection):
    """Uploads a single row of data to the given table."""
    cursor = connection.cursor()

    keys = sorted(row_dict.keys())
    vals = [row_dict[k] for k in keys]
    n_keys = len(keys)

    keys_template = ', '.join(['{}' for _ in range(n_keys)])
    vals_template = ', '.join(['%s' for _ in range(n_keys)])

    sql_ids = [sql.Identifier(table_name)] + [sql.Identifier(k) for k in keys]
    sql_str = sql.SQL(f'INSERT INTO {{}} ({keys_template}) VALUES ({vals_template})').format(*sql_ids)

    try:
        cursor.execute(sql_str, vals)
    except Exception as e:
        print(str(e))
        pass

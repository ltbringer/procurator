"""Initialize a database ready to be used.

Usage: seed.py --host=<host> --port=<port> --user=<user> --password=<password> --dbname=<dbname>

Options:
  -h --help              .
  --host=<host>          host at which postgres or its docker image is available.
  --port=<port>          port at which postgres is running.
  --user=<user>          User to use for init queries.
  --password=<password>  Password for the supplied --user.
  --dbname=<dbname>      The database to use.
"""
import psycopg2 as pg
from docopt import docopt
from procurator.utils.logger import L


def db_init(fn, host, port, password, user, dbname):
    conn = pg.connect(host=host, port=port, user=user, password=password, dbname=dbname)
    cursor = conn.cursor()
    fn(cursor)
    conn.commit()
    conn.close()


def sqlite_exec(sql_path, cursor, **kwargs):
    with open(sql_path, "r") as f:
        commands = f.read().split(";")
    for command in commands[:-1]:
        cursor.execute(command)


def create_tables(cursor):
    sqlite_exec("sql/create_tables.sql", cursor)
    L.info("Created tables: users, answers.")


def create_user(cursor):
    sqlite_exec("sql/create_user.sql", cursor)
    L.info("Created seed user.")


def create_answer(cursor):
    sqlite_exec("sql/create_answer.sql", cursor)
    L.info("Created seed answers.")


RECIPE = [create_tables, create_user, create_answer]


def main():
    arguments = docopt(__doc__)
    host = arguments["--host"]
    port = int(arguments["--port"])
    user = arguments["--user"]
    password = arguments["--password"]
    dbname = arguments["--dbname"]
    for recipe in RECIPE:
        db_init(recipe, host, port, user, password, dbname)

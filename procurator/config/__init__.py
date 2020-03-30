"""Database config setup.
"""
import os


DATABASE = {
    "host": os.environ.get("DB_HOST"),
    "port": os.environ.get("DB_PORT"),
    "password": os.environ.get("DB_PASSWORD"),
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER")
}

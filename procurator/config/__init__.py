import os


DB_DEV_CONFIG = {
    "host": os.environ.get("DB_HOST", "0.0.0.0"),
    "port": os.environ.get("DB_PORT", 7555),
    "password": os.environ.get("DB_PASSWORD", "procurator"),
    "dbname": os.environ.get("DB_NAME", "procurator"),
    "user": os.environ.get("DB_USER", "procurator")
}

DB_PROD_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "port": os.environ.get("DB_PORT"),
    "password": os.environ.get("DB_PASSWORD"),
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER")
}


DATABASE = {
    "dev": DB_DEV_CONFIG,
    "prod": DB_PROD_CONFIG
}

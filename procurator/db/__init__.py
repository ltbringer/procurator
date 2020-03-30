import os
import psycopg2 as pg
from procurator.config import DATABASE


def get_connection():
    config = DATABASE
    return pg.connect(host=config["host"], password=config["password"],
                      port=config["port"], dbname=config["dbname"],
                      user=config["user"])

def get_user_nicks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select id, nickname from users")
    return cursor.fetchall()

def get_user_knowledge(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    select id, questions, answers from answers
    where
    submitted_by = %(user_id)s
    """, {
        "user_id": user_id
    })
    return cursor.fetchall()

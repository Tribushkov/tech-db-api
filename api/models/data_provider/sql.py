import MySQLdb as db
from config import *


def connect():
    return db.connect(host=DB_HOST,
                      user=DB_USER,
                      passwd=DB_PASSWORD,
                      db=DB_NAME,
                      charset=DB_CHARSET)


def update_query(query, params):
    try:
        con = connect()
        cursor = con.cursor()
        cursor.execute(query, params)
        inserted_id = cursor.lastrowid
        con.commit()
        cursor.close()
    except db.Error:
        con.rollback()
        cursor.close()
        return STATUS_CODE['ALREADY_EXISTS']
    return inserted_id


def select_query(query, params):
    try:
        con = connect()
        cursor = con.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
    except db.Error:
        cursor.close()
        raise db.Error("Database error in usual query")
    return result


def select_query_dict(query, params):
    try:
        con = connect()
        cursor = con.cursor(db.cursors.DictCursor)
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        con.close()
    except db.Error:
        raise db.Error("Database error in dict query")
    return result


def execute(query):
    try:
        con = connect()
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        cursor.close()
    except db.Error:
        con.rollback()
    cursor.close()
    return


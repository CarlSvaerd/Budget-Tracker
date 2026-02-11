import sqlite3
import os


DB_NAME = "data/expenses.db"

def get_connection():

    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    
    return conn

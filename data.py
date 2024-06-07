import sqlite3
import tkinter as tk
from tkinter import ttk
from datetime import datetime

def initialize_db():
    conn = sqlite3.connect("trades.db")

    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
        )
        '''
    )

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        profit_loss REAL NOT NULL,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id)
        )
        '''
    )

    cursor.execute("PRAGMA table_info(trades)")
    columns = [info[1] for info in cursor.fetchall()]
    if "user_id" not in columns:
        cursor.execute("ALTER TABLE trades ADD COLUMN user_id INTEGER")

    cursor.execute("PRAGMA table_info(trades)")
    columns = [info[1] for info in cursor.fetchall()]
    if "timestamp" not in columns:
        cursor.execute("ALTER TABLE trades ADD COLUMN timestamp TEXT NO NULL")
        
        cursor.execute("UPDATE trades SET timestamp = date || ' 00:00:00' WHERE timestamp IS NULL")

    conn.commit()

    conn.close()

initialize_db()
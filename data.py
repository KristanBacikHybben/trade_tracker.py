import sqlite3
import app
import tkinter as tk
from tkinter import ttk

conn = sqlite3.connect("trades.db")

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY,
    date TEXT,
    profit_loss REAL
    )
    '''
)

conn.commit()

conn.close()
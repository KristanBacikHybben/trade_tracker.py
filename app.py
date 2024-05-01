import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from graphs import visualising_data

def submit_data():
    date = datetime.now().strftime("%d-%m-%Y")
    profit_loss = float(profit_loss_entry.get())

    conn = sqlite3.connect("trades.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO trades (date, profit_loss) VALUES (?, ?)", (date, profit_loss))
    conn.commit()

    profit_loss_entry.delete(0, tk.END)
    messagebox.showinfo("Done!", "Your data has been successfully submitted.")

def fetch_table_data():
    conn = sqlite3.connect("trades.db")
    cursor = conn.cursor()

    cursor.execute("SELECT date, profit_loss FROM trades")  
    data = cursor.fetchall()  

    conn.close()

    return data

root = tk.Tk()

window_width = 450
window_height = 300

root.geometry(f"{window_width}x{window_height}")

root.title("Trading tracker")

notebook = ttk.Notebook(root)
main_frame = tk.Frame(notebook)
notebook.add(main_frame, text="Tracker")

profit_loss = tk.Label(main_frame, text="Profit/Loss")
profit_loss.pack()

profit_loss_entry = tk.Entry(main_frame)
profit_loss_entry.pack()

submit_btn = tk.Button(main_frame, text="Submit", command=submit_data)
submit_btn.pack()

def show_data():
    frame_data = tk.Frame(notebook)
    notebook.add(frame_data, text="Data")

    tree = ttk.Treeview(frame_data)

    columns = ["date", "profit_loss"]
    tree["columns"] = columns

    tree.column("date", width=100)
    tree.heading("date", text="Date")

    tree.column("profit_loss", anchor=tk.W, width=100)
    tree.heading("profit_loss", text="Profit/Loss")

    def fill_treeview(data):
        for row in data:
            tree.insert("", tk.END, values=row)

    data = fetch_table_data()
    fill_treeview(data)

    tree.pack(expand=True, fill="both")

show_graph = tk.Button(main_frame, text="Show graph", command=visualising_data)
show_graph.pack()

show_data_button = ttk.Button(main_frame, text="Data", command=show_data)
show_data_button.pack()

notebook.pack(expand=True, fill="both")

root.mainloop()
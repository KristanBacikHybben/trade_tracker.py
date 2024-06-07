import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from graphs import visualising_data

window_width = 1080
window_height = 720

def register_user(username, password):
    conn = sqlite3.connect("trades.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect("trades.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ? AND PASSWORD = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return user[0]
    return None

def show_login_register(root):
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry(f"{window_width}x{window_height}")

    tk.Label(login_window, text="Username").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    def handle_register():
        username = username_entry.get()
        password = password_entry.get()
        if register_user(username, password):
            messagebox.showinfo("Successfully registered")
        else:
            messagebox.showerror("Error","username already exist")

    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        user_id = login_user(username, password)
        if user_id:
            login_window.destroy()
            root.deiconify()
            main(root,user_id)
        else:
            messagebox.showerror("Error","Wrong username or password")

    tk.Button(login_window, text="Login", command=handle_login).pack()
    tk.Button(login_window, text="Register", command=handle_register).pack()

def main(root, user_id):
    def submit_data():
        #date = datetime.now().strftime("%d-%m-%Y")
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        profit_loss = float(profit_loss_entry.get())

        conn = sqlite3.connect("trades.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO trades (timestamp, date, profit_loss, user_id) VALUES (?, ?, ?, ?)", (timestamp, timestamp.split()[0], profit_loss, user_id))
        conn.commit()

        profit_loss_entry.delete(0, tk.END)
        messagebox.showinfo("Done!", "Your data has been successfully submitted.")

    def fetch_table_data():
        conn = sqlite3.connect("trades.db")
        cursor = conn.cursor()

        cursor.execute("SELECT timestamp, profit_loss FROM trades WHERE user_id = ?", (user_id,))  
        data = cursor.fetchall()  

        conn.close()

        return data
    
    def logout():
        root.withdraw()
        show_login_register(root)

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

        columns = ["timestamp", "profit_loss"]
        tree["columns"] = columns

        tree.column("timestamp", width=100)
        tree.heading("timestamp", text="Timestamp")

        tree.column("profit_loss", anchor=tk.W, width=100)
        tree.heading("profit_loss", text="Profit/Loss")

        def fill_treeview(data):
            for row in data:
                tree.insert("", tk.END, values=row)

        data = fetch_table_data()
        fill_treeview(data)

        tree.pack(expand=True, fill="both")

    tk.Button(main_frame, text="Show graph", command=lambda: visualising_data(user_id)).pack()
    ttk.Button(main_frame, text="Data", command=show_data).pack()
    tk.Button(main_frame, text="Log out", command=logout).pack()

    notebook.pack(expand=True, fill="both")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    root.title("Trading Tracker")
    root.geometry(f"{window_width}x{window_height}")
    show_login_register(root)
    root.mainloop()
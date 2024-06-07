import sqlite3
import matplotlib.pyplot as plt

def visualising_data(user_id):
    conn = sqlite3.connect("trades.db")
    cursor = conn.cursor()

    cursor.execute("SELECT timestamp, profit_loss FROM trades WHERE user_id = ?", (user_id,))
    data = cursor.fetchall()

    timestamps = [d[0] for d in data]
    profit_loss = [d[1] for d in data]
    
    plt.figure(figsize=(10,5))
    plt.plot(timestamps, profit_loss, "o", label="Profit/Loss", linestyle="--")

    for timestamp, value in zip(timestamps, profit_loss):
        color = "green" if value >= 0 else "red"
        plt.text(timestamp, value, f"{value}", fontsize=12, ha="right", va="bottom", color=color)
    
    plt.xlabel("Timestamp")
    plt.ylabel("Profit/Loss")
    plt.title("Trades")
    plt.legend()
    plt.show()

    conn.close()
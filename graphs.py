import sqlite3
import matplotlib.pyplot as plt

def visualising_data():
    conn = sqlite3.connect("trades.db")
    cursor = conn.cursor()

    cursor.execute("SELECT date, profit_loss FROM trades")
    data = cursor.fetchall()

    dates = [d[0] for d in data]
    profit_loss = [d[1] for d in data]
    
    plt.figure(figsize=(10,5))
    plt.plot(dates, profit_loss, "o", label="Profit/Loss", linestyle="--")

    for date, value in zip(dates, profit_loss):
        color = "green" if value >= 0 else "red"
        plt.text(date, value, f"{value}", fontsize=12, ha="right", va="bottom", color=color)
    
    plt.xlabel("Date")
    plt.ylabel("Profit/Loss")
    plt.title("Trades")
    plt.legend()
    plt.show()

    conn.close()
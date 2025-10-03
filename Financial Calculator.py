import tkinter as tk
from tkinter import messagebox
import yfinance as yf

# --- Functions ---
def calculate_npv(cash_flows, discount_rate):
    npv = 0
    for t, cf in enumerate(cash_flows):
        npv += cf / ((1 + discount_rate) ** t)
    return npv

def calculate_irr(cash_flows, max_iterations=1000, tolerance=1e-6):
    low, high = -1.0, 1.0
    for _ in range(max_iterations):
        guess = (low + high) / 2
        npv = calculate_npv(cash_flows, guess)
        if abs(npv) < tolerance:
            return guess
        if npv > 0:
            low = guess
        else:
            high = guess
    return guess

def fetch_stock_data():
    try:
        ticker = ticker_entry.get().strip().upper()
        if not ticker:
            raise ValueError("Please enter a stock ticker symbol.")
        
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        
        if hist.empty:
            raise ValueError("No data found for this ticker.")
        
        latest_price = hist["Close"].iloc[-1]
        messagebox.showinfo("Stock Price", f"{ticker} Latest Close Price: ${latest_price:.2f}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not fetch stock data: {e}")

def calculate_financials():
    try:
        discount_rate = float(discount_rate_entry.get()) / 100
        initial_investment = float(investment_entry.get())
        cash_flows = [initial_investment]

        years = int(years_entry.get())
        for i in range(years):
            cf = float(cash_flow_entries[i].get())
            cash_flows.append(cf)

        npv = calculate_npv(cash_flows, discount_rate)
        irr = calculate_irr(cash_flows)

        result = (
            f"NPV: {npv:.2f}\n"
            f"IRR: {irr:.2%}\n"
        )
        if npv > 0:
            result += "✅ NPV is positive: ACCEPT the project.\n"
        else:
            result += "❌ NPV is negative: REJECT the project.\n"
        if irr > discount_rate:
            result += "✅ IRR is greater than the discount rate: Good investment."
        else:
            result += "❌ IRR is less than the discount rate: Not attractive."

        messagebox.showinfo("Results", result)

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

def generate_cash_flow_entries():
    for widget in cash_flow_frame.winfo_children():
        widget.destroy()
    cash_flow_entries.clear()

    years = int(years_entry.get())
    for i in range(years):
        label = tk.Label(cash_flow_frame, text=f"Year {i+1} Cash Flow:")
        label.grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(cash_flow_frame)
        entry.grid(row=i, column=1, padx=5, pady=5)
        cash_flow_entries.append(entry)

# --- GUI Setup ---
root = tk.Tk()
root.title("Stock & Investment Calculator")

# Stock ticker input
tk.Label(root, text="Stock Ticker (Yahoo Finance)").grid(row=0, column=0, padx=5, pady=5)
ticker_entry = tk.Entry(root)
ticker_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Fetch Stock Price", command=fetch_stock_data).grid(row=0, column=2, padx=5, pady=5)

# Discount rate & investment
tk.Label(root, text="Discount Rate (%)").grid(row=1, column=0, padx=5, pady=5)
discount_rate_entry = tk.Entry(root)
discount_rate_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Initial Investment (negative)").grid(row=2, column=0, padx=5, pady=5)
investment_entry = tk.Entry(root)
investment_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Number of Years").grid(row=3, column=0, padx=5, pady=5)
years_entry = tk.Entry(root)
years_entry.grid(row=3, column=1, padx=5, pady=5)

# Cash flow section
cash_flow_frame = tk.Frame(root)
cash_flow_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
cash_flow_entries = []

tk.Button(root, text="Set Years", command=generate_cash_flow_entries).grid(row=5, column=0, columnspan=3, pady=10)
tk.Button(root, text="Calculate NPV & IRR", command=calculate_financials).grid(row=6, column=0, columnspan=3, pady=10)

root.mainloop()
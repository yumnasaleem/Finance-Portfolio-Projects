import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from matplotlib.dates import DateFormatter, MonthLocator, WeekdayLocator

def fetch_and_plot_data(stock_symbol, root_frame):
    for widget in root_frame.winfo_children():
        widget.destroy()

    try:
        stock = yf.Ticker(stock_symbol)
        hist = stock.history(period="1y")

        if hist.empty:
            messagebox.showerror("Error", f"Could not fetch data for {stock_symbol}. Please check the symbol.")
            return

        # --- Create Matplotlib Figure and Subplots (1 Row, 3 Columns) ---
        # Adjusted figsize for horizontal layout. Wider, less height per chart.
        fig, axs = plt.subplots(1, 3, figsize=(20, 7), facecolor='black') # 1 row, 3 columns
        fig.patch.set_facecolor('black')

        # Set common style for all axes
        for i, ax in enumerate(axs):
            ax.set_facecolor('black')
            ax.tick_params(axis='x', colors='white', labelsize=9) # Slightly smaller labels for horizontal fit
            ax.tick_params(axis='y', colors='white', labelsize=9)
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
            ax.title.set_fontsize(14) # Slightly smaller title font
            ax.set_xlabel('Date', color='white', fontsize=10)
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.grid(True, linestyle='--', alpha=0.2, color='gray')

            # Date formatting for x-axis
            ax.xaxis.set_major_formatter(DateFormatter('%Y-%m')) # Shorter date format for horizontal layout
            ax.xaxis.set_major_locator(MonthLocator(interval=2)) # Show every other month
            ax.xaxis.set_minor_locator(MonthLocator())

            # Rotate x-tick labels for all subplots in horizontal view
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right', rotation_mode="anchor")


        # 1. Line Graph (Closing Price) - Leftmost
        axs[0].plot(hist.index, hist['Close'], color='cyan', linewidth=2)
        axs[0].set_title(f'{stock_symbol} Close Price (1 Year)', color='white', fontsize=16)
        axs[0].set_ylabel('Price (USD)', color='white', fontsize=12)


        # 2. Column Graph (Volume) - Middle
        axs[1].bar(hist.index, hist['Volume'], color='purple', alpha=0.7, width=0.8)
        axs[1].set_title(f'{stock_symbol} Trading Volume', color='white', fontsize=16)
        axs[1].set_ylabel('Volume', color='white', fontsize=12)
        axs[1].ticklabel_format(style='plain', axis='y')
        axs[1].yaxis.get_major_formatter().set_scientific(False)


        # 3. Pie Chart (Daily Change Distribution) - Rightmost
        hist['Daily_Change'] = hist['Close'].diff()
        up_days = (hist['Daily_Change'] > 0).sum()
        down_days = (hist['Daily_Change'] < 0).sum()
        no_change_days = (hist['Daily_Change'] == 0).sum()

        change_data = [up_days, down_days, no_change_days]
        labels = ['Up Days', 'Down Days', 'No Change Days']
        colors = ['#8BC34A', '#F44336', '#9E9E9E']
        explode = [0.05, 0.05, 0.05]

        wedges, texts, autotexts = axs[2].pie(change_data, labels=labels, colors=colors, autopct='%1.1f%%',
                                             startangle=90, textprops={'color': 'white', 'fontsize': 10},
                                             explode=explode, pctdistance=0.75, labeldistance=1.1,
                                             wedgeprops={'edgecolor': 'black', 'linewidth': 1})
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontsize(9) # Smaller font for pie percentages
        axs[2].set_title(f'{stock_symbol} Daily Change Dist.', color='white', fontsize=16)
        axs[2].axis('equal')


        plt.tight_layout(rect=[0, 0.05, 1, 0.95], w_pad=2.0) # Increased w_pad (width padding)
        fig.autofmt_xdate(bottom=0.2, rotation=45, ha='right')


        # --- Investment Suggestion (unchanged position, but wider wraplength) ---
        suggestion_label = tk.Label(root_frame, text="", bg="black", fg="white", font=("Arial", 14, "bold"), wraplength=1200) # Increased wraplength
        suggestion_label.pack(pady=(10, 25))

        latest_close = hist['Close'].iloc[-1]
        previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else latest_close
        if latest_close > previous_close:
            suggestion = "Based on recent performance, the stock showed an upward trend today. Further analysis is recommended before investing."
            suggestion_label.config(fg="#8BC34A")
        elif latest_close < previous_close:
            suggestion = "Based on recent performance, the stock showed a downward trend today. Consider caution and further research."
            suggestion_label.config(fg="#F44336")
        else:
            suggestion = "The stock price remained stable today. Comprehensive research is advisable."
            suggestion_label.config(fg="#9E9E9E")

        suggestion_label.config(text=f"Investment Insight: {suggestion}")


        # --- Embed Matplotlib plot into Tkinter ---
        canvas = FigureCanvasTkAgg(fig, master=root_frame)
        canvas_widget = canvas.get_tk_widget()
        # Pack to occupy available space, centered if possible
        canvas_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        canvas.draw()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}. Please ensure the stock symbol is valid and you have an internet connection.")
        for widget in root_frame.winfo_children():
            widget.destroy()
        tk.Label(root_frame, text="Error loading data. Please try again with a valid symbol and internet connection.",
                 bg="black", fg="red", font=("Arial", 16)).pack(pady=50)

def create_dashboard_gui():
    root = tk.Tk()
    root.title("Stock Dashboard")
    # Significantly wider window for horizontal charts
    root.geometry("1400x800") # Increased width, reduced height
    root.configure(bg="black")

    # Input Frame (remains at top)
    input_frame = tk.Frame(root, bg="black", pady=15)
    input_frame.pack(side=tk.TOP, fill=tk.X)

    tk.Label(input_frame, text="Enter Stock Symbol (e.g., AAPL, GOOGL):",
             bg="black", fg="white", font=("Arial", 13)).pack(side=tk.LEFT, padx=15)

    stock_entry = ttk.Entry(input_frame, width=15, font=("Arial", 13))
    stock_entry.pack(side=tk.LEFT, padx=10)
    stock_entry.bind("<Return>", lambda event: fetch_and_plot_data(stock_entry.get().upper(), plot_frame))


    plot_frame = tk.Frame(root, bg="black")
    plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=15, pady=15)

    # Initial placeholder
    tk.Label(plot_frame, text="Enter a stock symbol and press Enter or click 'Show Dashboard' to see the charts.",
             bg="black", fg="gray", font=("Arial", 18)).pack(pady=70)

    # Submit Button
    submit_button = ttk.Button(input_frame, text="Show Dashboard",
                               command=lambda: fetch_and_plot_data(stock_entry.get().upper(), plot_frame))
    submit_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()

if __name__ == "__main__":
    create_dashboard_gui()
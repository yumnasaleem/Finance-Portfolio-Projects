import tkinter as tk
from tkinter import simpledialog, messagebox
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Function to fetch stock data and forecast
def forecast_stock():
    try:
        ticker = simpledialog.askstring("Input", "Enter Stock Ticker (e.g., MSFT, AAPL, TSLA):")
        steps = simpledialog.askinteger("Input", "Enter number of days to forecast:", minvalue=1, maxvalue=365)

        if not ticker or not steps:
            messagebox.showerror("Error", "Ticker and forecast steps are required!")
            return

        # Download stock data
        data = yf.download(ticker, start="2015-01-01")

        # Pick price column safely
        if "Adj Close" in data.columns:
            series = data["Adj Close"].dropna()
        elif "Close" in data.columns:
            series = data["Close"].dropna()
        else:
            messagebox.showerror("Error", "No valid price column found in data!")
            return

        if series.empty:
            messagebox.showerror("Error", f"No data found for ticker: {ticker}")
            return

        # Fit ARIMA model
        model = ARIMA(series, order=(5, 1, 0))
        fitted_model = model.fit()

        # Forecast
        forecast = fitted_model.forecast(steps=steps)
        last_date = series.index[-1]
        future_dates = pd.date_range(start=last_date, periods=steps+1, freq="B")[1:]
        forecast = pd.Series(forecast.values, index=future_dates)

        # Print forecast values in console
        print("\nForecasted Values:")
        print(forecast)

        # Show forecast values in popup (limit to first 10 to avoid very long messages)
        preview = forecast.head(10).to_string()
        messagebox.showinfo("Forecast Results", f"First forecasted values:\n\n{preview}\n\nCheck console for full list.")

        # Plot results
        plt.figure(figsize=(12, 6))
        plt.plot(series, label="Historical Prices")
        plt.plot(forecast, label="Forecast", color="red")
        plt.title(f"{ticker} Stock Price Forecast ({steps} Days)")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Tkinter window setup
root = tk.Tk()
root.withdraw()  # Hide the empty Tkinter root window

forecast_stock()
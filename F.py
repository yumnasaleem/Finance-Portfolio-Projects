import tkinter as tk
from tkinter import messagebox

# --- Functions ---
def calculate():
    try:
        SP = float(entry_SP.get())
        MP = float(entry_MP.get())
        role = role_var.get().lower()

        if role == "buyer":
            result = MP - SP
            if result > 0:
                messagebox.showinfo("Result", f"Buyer: Profit = {result}")
            elif result < 0:
                messagebox.showinfo("Result", f"Buyer: Loss = {result}")
            else:
                messagebox.showinfo("Result", "Buyer: Breakeven")
        elif role == "seller":
            result = SP - MP
            if result > 0:
                messagebox.showinfo("Result", f"Seller: Profit = {result}")
            elif result < 0:
                messagebox.showinfo("Result", f"Seller: Loss = {result}")
            else:
                messagebox.showinfo("Result", "Seller: Breakeven")
        else:
            messagebox.showwarning("Error", "Please select Buyer or Seller")

    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers for SP and MP")

# --- GUI Layout ---
root = tk.Tk()
root.title("Profit/Loss Calculator")
root.geometry("350x250")

# Labels and Entries
tk.Label(root, text="Selling Price (SP):").pack(pady=5)
entry_SP = tk.Entry(root)
entry_SP.pack(pady=5)

tk.Label(root, text="Market Price (MP):").pack(pady=5)
entry_MP = tk.Entry(root)
entry_MP.pack(pady=5)

# Radio buttons for Buyer/Seller
role_var = tk.StringVar()
tk.Label(root, text="Choose Role:").pack(pady=5)
tk.Radiobutton(root, text="Buyer", variable=role_var, value="buyer").pack()
tk.Radiobutton(root, text="Seller", variable=role_var, value="seller").pack()

# Calculate button
tk.Button(root, text="Calculate", command=calculate).pack(pady=15)

# Run the app
root.mainloop()

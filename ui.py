import tkinter as tk
from tkinter import ttk, messagebox
from converter import CurrencyConverter

class CurrencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💱 Currency Converter")
        self.root.geometry("500x600")
        self.root.configure(bg="#f0f4f7")

        self.converter = CurrencyConverter()

        # Currency Variables
        self.from_currency = tk.StringVar()
        self.amount = tk.StringVar()
        self.dark_mode = False

        self.currency_list = [
            "USD", "EUR", "GBP", "INR", "JPY", "CAD", "AUD", "CNY", "NZD",
            "CHF", "SGD", "HKD", "ZAR", "RUB", "BRL", "MXN", "SEK", "TRY", "AED"
        ]
        self.from_currency.set("USD")

        self.create_widgets()

    def create_widgets(self):
        header = tk.Label(self.root, text="💱 Currency Converter", font=("Segoe UI", 18, "bold"), fg="#003366", bg="#f0f4f7")
        header.pack(pady=10)

        frame = tk.Frame(self.root, bg="#f0f4f7")
        frame.pack(pady=10)

        tk.Label(frame, text="Amount:", font=("Segoe UI", 12), bg="#f0f4f7").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(frame, textvariable=self.amount, font=("Segoe UI", 12), width=22).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="From Currency:", font=("Segoe UI", 12), bg="#f0f4f7").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        from_box = ttk.Combobox(frame, values=self.currency_list, textvariable=self.from_currency, state="readonly", font=("Segoe UI", 11))
        from_box.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame, text="To Currencies:", font=("Segoe UI", 12), bg="#f0f4f7").grid(row=2, column=0, padx=10, pady=5, sticky="ne")
        self.to_currency_listbox = tk.Listbox(frame, selectmode="multiple", height=10, exportselection=0, font=("Segoe UI", 10))
        for currency in self.currency_list:
            self.to_currency_listbox.insert(tk.END, currency)
        self.to_currency_listbox.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Converted Results:", font=("Segoe UI", 12, "bold"), bg="#f0f4f7").pack(pady=(10, 0))
        result_frame = tk.Frame(self.root, bg="#f0f4f7")
        result_frame.pack(pady=5)

        self.result_box = tk.Text(result_frame, height=10, width=50, font=("Consolas", 11))
        self.result_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(result_frame, command=self.result_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_box.config(yscrollcommand=scrollbar.set)

        button_frame = tk.Frame(self.root, bg="#f0f4f7")
        button_frame.pack(pady=10)

        convert_btn = tk.Button(button_frame, text="Convert", font=("Segoe UI", 12), command=self.convert_currency, bg="#cceeff", width=12)
        convert_btn.grid(row=0, column=0, padx=10)

        clear_btn = tk.Button(button_frame, text="Clear", font=("Segoe UI", 12), command=self.clear_all, bg="#ffcccc", width=12)
        clear_btn.grid(row=0, column=1, padx=10)

        toggle_theme = tk.Button(self.root, text="Toggle Dark Mode", command=self.toggle_dark_mode, bg="#e0e0e0", font=("Segoe UI", 10))
        toggle_theme.pack(pady=10)

    def convert_currency(self):
        self.result_box.delete('1.0', tk.END)
        try:
            amount = float(self.amount.get())
            from_curr = self.from_currency.get()
            indices = self.to_currency_listbox.curselection()
            if not indices:
                messagebox.showwarning("Select Currency", "Please select at least one target currency.")
                return
            to_currencies = [self.currency_list[i] for i in indices]
            results = self.converter.multi_convert(amount, from_curr, to_currencies)
            for curr, val in results.items():
                self.result_box.insert(tk.END, f"{amount} {from_curr} → {val} {curr}\n")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a numeric value.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_all(self):
        self.amount.set("")
        self.result_box.delete('1.0', tk.END)
        self.from_currency.set("USD")
        self.to_currency_listbox.selection_clear(0, tk.END)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        bg_color = "#1e1e1e" if self.dark_mode else "#f0f4f7"
        fg_color = "#ffffff" if self.dark_mode else "#000000"

        self.root.configure(bg=bg_color)
        for widget in self.root.winfo_children():
            try:
                widget.configure(bg=bg_color, fg=fg_color)
            except:
                pass

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyApp(root)
    root.mainloop()

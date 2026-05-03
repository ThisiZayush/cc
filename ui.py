import tkinter as tk
from tkinter import ttk, messagebox
# Ensure your converter.py file is in the same directory
from converter import CurrencyConverter 

class CurrencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💱 Currency Converter Pro")
        self.root.geometry("480x700")
        self.root.configure(bg="#F8FAFC") # Modern off-white background

        self.converter = CurrencyConverter()

        # State Variables
        self.from_currency = tk.StringVar()
        self.amount = tk.StringVar()
        self.dark_mode = False

        self.currency_list = [
            "USD", "EUR", "GBP", "INR", "JPY", "CAD", "AUD", "CNY", "NZD",
            "CHF", "SGD", "HKD", "ZAR", "RUB", "BRL", "MXN", "SEK", "TRY", "AED"
        ]
        self.from_currency.set("USD")

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        """Define custom styles for ttk widgets"""
        self.style = ttk.Style()
        self.style.theme_use('clam') # Use 'clam' as a base for better customization
        
        # Configure TCombobox
        self.style.configure("TCombobox", fieldbackground="white", background="#F8FAFC")

    def create_widgets(self):
        # Header Section
        self.header_frame = tk.Frame(self.root, bg="#0F172A", height=80)
        self.header_frame.pack(fill=tk.X)
        
        self.header_label = tk.Label(
            self.header_frame, text="CURRENCY CONVERTER", 
            font=("Helvetica", 16, "bold"), fg="#FFFFFF", bg="#0F172A"
        )
        self.header_label.pack(pady=25)

        # Main Container
        self.main_container = tk.Frame(self.root, bg="#F8FAFC", padx=30, pady=20)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Input Section
        self.lbl_amount = tk.Label(self.main_container, text="Amount to Convert", font=("Arial", 10, "bold"), bg="#F8FAFC", fg="#64748B")
        self.lbl_amount.pack(anchor="w", pady=(0, 5))
        
        self.entry_amount = tk.Entry(
            self.main_container, textvariable=self.amount, font=("Arial", 14), 
            bg="white", relief="flat", highlightthickness=1, highlightbackground="#CBD5E1"
        )
        self.entry_amount.pack(fill=tk.X, ipady=8, pady=(0, 20))

        # Dropdown Section
        self.lbl_from = tk.Label(self.main_container, text="From Currency", font=("Arial", 10, "bold"), bg="#F8FAFC", fg="#64748B")
        self.lbl_from.pack(anchor="w", pady=(0, 5))
        
        self.from_box = ttk.Combobox(self.main_container, values=self.currency_list, textvariable=self.from_currency, state="readonly", font=("Arial", 11))
        self.from_box.pack(fill=tk.X, ipady=5, pady=(0, 20))

        # Listbox Section
        self.lbl_to = tk.Label(self.main_container, text="Convert To (Select Multiple)", font=("Arial", 10, "bold"), bg="#F8FAFC", fg="#64748B")
        self.lbl_to.pack(anchor="w", pady=(0, 5))
        
        self.to_currency_listbox = tk.Listbox(
            self.main_container, selectmode="multiple", height=6, 
            font=("Arial", 10), relief="flat", borderwidth=0, highlightthickness=1, highlightbackground="#CBD5E1"
        )
        for currency in self.currency_list:
            self.to_currency_listbox.insert(tk.END, currency)
        self.to_currency_listbox.pack(fill=tk.X)

        # Results Section
        tk.Label(self.main_container, text="Results", font=("Arial", 10, "bold"), bg="#F8FAFC", fg="#64748B").pack(anchor="w", pady=(15, 5))
        
        self.res_frame = tk.Frame(self.main_container, bg="white", highlightthickness=1, highlightbackground="#CBD5E1")
        self.res_frame.pack(fill=tk.BOTH, expand=True)

        self.result_box = tk.Text(self.res_frame, height=5, font=("Consolas", 11), bg="white", relief="flat", padx=10, pady=10)
        self.result_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Buttons Section
        self.btn_frame = tk.Frame(self.main_container, bg="#F8FAFC")
        self.btn_frame.pack(fill=tk.X, pady=20)

        self.convert_btn = tk.Button(
            self.btn_frame, text="Convert Now", font=("Arial", 11, "bold"), 
            command=self.convert_currency, bg="#2563EB", fg="white", 
            relief="flat", cursor="hand2", activebackground="#1D4ED8", activeforeground="white"
        )
        self.convert_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5), ipady=10)

        self.clear_btn = tk.Button(
            self.btn_frame, text="Clear", font=("Arial", 11, "bold"), 
            command=self.clear_all, bg="#E2E8F0", fg="#475569", 
            relief="flat", cursor="hand2"
        )
        self.clear_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0), ipady=10)

        self.toggle_theme = tk.Button(
            self.root, text="🌓 Toggle Dark Mode", font=("Arial", 9),
            command=self.toggle_dark_mode, bg="#F1F5F9", relief="flat", fg="#475569"
        )
        self.toggle_theme.pack(pady=(0, 20))

    def convert_currency(self):
        self.result_box.delete('1.0', tk.END)
        try:
            amount = float(self.amount.get())
            from_curr = self.from_currency.get()
            indices = self.to_currency_listbox.curselection()
            if not indices:
                messagebox.showwarning("Selection Missing", "Please select at least one target currency.")
                return
            
            to_currencies = [self.currency_list[i] for i in indices]
            results = self.converter.multi_convert(amount, from_curr, to_currencies)
            
            for curr, val in results.items():
                self.result_box.insert(tk.END, f" {amount} {from_curr}  ➜  {val} {curr}\n")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert: {str(e)}")

    def clear_all(self):
        self.amount.set("")
        self.result_box.delete('1.0', tk.END)
        self.from_currency.set("USD")
        self.to_currency_listbox.selection_clear(0, tk.END)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        
        # Colors
        bg_main = "#1E293B" if self.dark_mode else "#F8FAFC"
        bg_card = "#0F172A" if self.dark_mode else "white"
        fg_text = "#F1F5F9" if self.dark_mode else "#64748B"
        fg_header = "#38BDF8" if self.dark_mode else "#FFFFFF"

        # Apply Colors
        self.root.configure(bg=bg_main)
        self.main_container.configure(bg=bg_main)
        self.btn_frame.configure(bg=bg_main)
        
        # Update Labels
        for widget in [self.lbl_amount, self.lbl_from, self.lbl_to]:
            widget.configure(bg=bg_main, fg=fg_text)
        
        # Update Input/List/Text
        self.entry_amount.configure(bg=bg_card, fg="white" if self.dark_mode else "black", insertbackground="white" if self.dark_mode else "black")
        self.to_currency_listbox.configure(bg=bg_card, fg="white" if self.dark_mode else "black")
        self.result_box.configure(bg=bg_card, fg="#38BDF8" if self.dark_mode else "black")
        self.res_frame.configure(bg=bg_card)
        
        # Update Header
        self.header_frame.configure(bg="#020617" if self.dark_mode else "#0F172A")
        self.header_label.configure(bg="#020617" if self.dark_mode else "#0F172A", fg=fg_header)
        
        # Update Buttons
        self.toggle_theme.configure(bg=bg_card, fg=fg_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyApp(root)
    root.mainloop()
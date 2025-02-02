import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import io
from PIL import Image, ImageTk


class CryptoTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Cryptocurrency Tracker")

        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 12), padding=10)
        self.style.configure('TButton', font=('Arial', 12), padding=10)
        self.style.configure('TCombobox', font=('Arial', 12), padding=10)

        # Predefined list of cryptocurrencies
        self.crypto_symbols = {
            'Bitcoin': 'BTC-USD',
            'Ethereum': 'ETH-USD',
            'Ripple': 'XRP-USD',
            'Litecoin': 'LTC-USD',
            'Cardano': 'ADA-USD',
            'Solana': 'SOL-USD',
            'Dogecoin': 'DOGE-USD',
            'Polkadot': 'DOT-USD',
            'Chainlink': 'LINK-USD',
            'Polygon': 'MATIC-USD'
        }

        # UI components
        self.label = ttk.Label(root, text="Select Cryptocurrency:")
        self.label.pack(pady=10)

        self.symbol_combobox = ttk.Combobox(root, values=list(self.crypto_symbols.keys()))
        self.symbol_combobox.pack(pady=5)

        self.fetch_button = ttk.Button(root, text="Fetch Data", command=self.fetch_data)
        self.fetch_button.pack(pady=5)

        self.save_button = ttk.Button(root, text="Save Data to CSV", command=self.save_data)
        self.save_button.pack(pady=5)

        self.plot_button = ttk.Button(root, text="Show Graph", command=self.show_graph)
        self.plot_button.pack(pady=5)

        self.crypto_data = None
        self.symbol = None

    def fetch_data(self):
        selected_crypto = self.symbol_combobox.get().strip()
        if not selected_crypto:
            messagebox.showerror("Error", "Please select a cryptocurrency.")
            return
        
        symbol = self.crypto_symbols.get(selected_crypto, None)
        if not symbol:
            messagebox.showerror("Error", "Invalid cryptocurrency selected.")
            return
        
        try:
            # Fetch data from Yahoo Finance
            self.crypto_data = yf.download(symbol, period="1mo", interval="1d")
            self.symbol = selected_crypto
            if self.crypto_data.empty:
                messagebox.showerror("Error", f"No data found for {selected_crypto}.")
            else:
                messagebox.showinfo("Success", f"Data fetched for {selected_crypto}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data: {e}")

    def save_data(self):
        if self.crypto_data is None:
            messagebox.showerror("Error", "No data to save. Please fetch data first.")
            return
        
        # Save data to CSV
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Save CSV File"
        )
        if file_path:
            try:
                self.crypto_data.to_csv(file_path)
                messagebox.showinfo("Success", f"Data saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save data: {e}")

    def show_graph(self):
        if self.crypto_data is None:
            messagebox.showerror("Error", "No data to plot. Please fetch data first.")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(self.crypto_data.index, self.crypto_data['Close'], marker='o', color='blue')
        plt.title(f'{self.symbol} Closing Prices', fontsize=14)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Closing Price (USD)', fontsize=12)
        plt.grid(True)
        plt.tight_layout()

        # Save the graph to a BytesIO object
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png')
        img_bytes.seek(0)
        plt.close()

        # Load the image and show it
        img = Image.open(img_bytes)
        img.thumbnail((800, 400))  # Resize image to fit in the Tkinter window
        img_tk = ImageTk.PhotoImage(img)

        # Create a new window to display the graph
        graph_window = tk.Toplevel(self.root)
        graph_window.title(f"{self.symbol} Graph")
        panel = tk.Label(graph_window, image=img_tk)
        panel.image = img_tk  # Keep a reference to avoid garbage collection
        panel.pack()


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoTracker(root)
    root.mainloop()

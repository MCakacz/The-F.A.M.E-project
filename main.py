import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

# Klucz API do serwisu finansowego (np. Alpha Vantage) 
#tu macie link do otrzymania klucza api ----> https://www.alphavantage.co/support/#api-key
API_KEY = "TWOJ_KLUCZ_API"

def get_stock_price(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if "Time Series (1min)" in data:
        latest_data = list(data["Time Series (1min)"].values())[0]
        return latest_data["1. open"]
    else:
        return None

def plot_stock_price(symbol, prices):
    timestamps = list(prices.keys())
    values = [float(price["1. open"]) for price in prices.values()]
    datetime_objects = [datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") for timestamp in timestamps]

    root = tk.Tk()
    root.title(f"Wykres ({symbol})")
    
    # Zablokowanie zmiany rozmiaru okna
    root.resizable(False, False)

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(datetime_objects, values, label=symbol)
    ax.set_title(f"Cena akcji {symbol}")
    ax.set_xlabel("Czas")
    ax.set_ylabel("Cena (USD)")
    ax.legend()
    ax.grid(True)
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()
    
    # Obsługa zamknięcia okna
    def on_closing():
        if tk.messagebox.askokcancel("Zamknij program", "Czy na pewno chcesz zamknąć program?"):
            root.destroy()
            main()  # Ponowne wywołanie głównej funkcji
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()

def main():
    print("Witaj w asystencie finansowym!")
    
    while True:
        print("\nCo chciałbyś zrobić?")
        print("1. Sprawdź cenę akcji")
        print("2. Wyjdź z programu")
        
        choice = input("Wybierz opcję (1/2): ")
        
        if choice == "1":
            symbol = input("Podaj symbol akcji (np. AAPL): ")
            price = get_stock_price(symbol)
            if price:
                print(f"Aktualna cena akcji {symbol}: {price} USD")
                
                # Pobieranie danych cen akcji na potrzeby wykresu
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}"
                response = requests.get(url)
                data = response.json()
                if "Time Series (1min)" in data:
                    prices = data["Time Series (1min)"]
                    plot_stock_price(symbol, prices)
                else:
                    print("Nie można pobrać danych do wykresu.")
            else:
                print(f"Nie można pobrać ceny dla {symbol}. Sprawdź poprawność symbolu.")
        elif choice == "2":
            if input("Czy na pewno chcesz wyjść z programu? (Tak/Nie): ").strip().lower() == "tak":
                print("Dziękujemy za skorzystanie z asystenta finansowego F.A.M.E | Do widzenia!")
                sys.exit()  # Zakończ program
        else:
            print("Nieprawidłowy wybór. Wybierz 1 lub 2.")

if __name__ == "__main__":
    main()

import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://v6.exchangerate-api.com/v6"

CACHE_FILE = "exchange_rates.json"

class CurrencyConverter:
    def __init__(self):
        self.cache = {}
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r") as f:
                    self.cache = json.load(f)
            except json.JSONDecodeError:
                self.cache = {}

    def _save_cache(self):
        with open(CACHE_FILE, "w") as f:
            json.dump(self.cache, f, indent=2)

    def fetch_rates(self, base_currency):
        try:
            url = f"{BASE_URL}/{API_KEY}/latest/{base_currency}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            if "conversion_rates" not in data:
                raise ValueError("Invalid API response")

            rates = data["conversion_rates"]
            self.cache[base_currency] = {
                "rates": rates
            }
            self._save_cache()
            return rates

        except Exception as e:
            print(f"[WARNING] API fetch failed: {e}")
            if base_currency in self.cache:
                return self.cache[base_currency]["rates"]
            raise RuntimeError(f"No data for base currency: {base_currency}")

    def convert(self, amount, from_currency, to_currency):
        rates = self.fetch_rates(from_currency)
        if to_currency not in rates:
            raise KeyError(f"Rate not available for {to_currency}")
        return round(amount * rates[to_currency], 2)

    def multi_convert(self, amount, from_currency, to_currencies):
        rates = self.fetch_rates(from_currency)
        results = {}
        for currency in to_currencies:
            if currency in rates:
                results[currency] = round(amount * rates[currency], 2)
            else:
                results[currency] = "N/A"
        return results

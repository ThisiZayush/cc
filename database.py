import json
import os
from datetime import datetime

CACHE_FILE = "exchange_rates.json"

class OfflineMode:
    def __init__(self):
        self.cache = {}
        self.load_rates()

    def save_rates(self, base_currency, data):
        """Save exchange rates for a specific base currency"""
        self.cache[base_currency] = {
            "timestamp": datetime.now().isoformat(),
            "rates": data["rates"]
        }
        with open(CACHE_FILE, "w") as file:
            json.dump(self.cache, file)

    def load_rates(self):
        """Load cached exchange rates if available"""
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r") as file:
                    self.cache = json.load(file)
            except Exception:
                self.cache = {}

    def get_rates(self, base_currency):
        """Get cached rates for a given base currency"""
        if base_currency in self.cache:
            return self.cache[base_currency]["rates"]
        return None

    def is_cached(self, base_currency):
        return base_currency in self.cache

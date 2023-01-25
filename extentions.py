import json
import requests
from config import keys

class APIExeption(Exception):
    pass

class CriptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIExeption(f"Невозможно перевести одинаковые валюты {base}.")
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIExeption(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIExeption(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIExeption(f"Не удалось обработать количество {amount}")

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base
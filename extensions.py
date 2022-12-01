import requests
import json
from config import *

class ExchangeException(Exception):
    pass

class Exchange:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise ExchangeException(f'Нельзя осуществить конвертацию валюты {base} саму в себя.')

        try:
            base_ticker = currencies[base]
        except KeyError:
            raise ExchangeException(f'Не вышло обработать валюту {base}')

        try:
            quote_ticker = currencies[quote]
        except KeyError:
            raise ExchangeException(f'Не вышло обработать валюту {quote}')

        try:
            amount = int(amount)
        except ValueError:
            raise ExchangeException(f'Не вышло обработать количество {amount}')

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = float(json.loads(r.content)[currencies[quote]])
        return total_base
import requests
# import json
from config import keys, tickers, xpath_
import lxml.html
from lxml import etree


class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно конвертировать оинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        if f"{quote_ticker}/{base_ticker}" in ['USD/RUB', 'EUR/RUB', 'EUR/USD']:
            html = requests.get(tickers[f"{quote_ticker}/{base_ticker}"]).content
            tree = lxml.html.document_fromstring(html)
            total_base = tree.xpath(xpath_)[1]
            total_base = total_base.replace(',', '.')

        # r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        # total_base = json.loads(r.content)[keys[base]]
        return float(total_base) * amount
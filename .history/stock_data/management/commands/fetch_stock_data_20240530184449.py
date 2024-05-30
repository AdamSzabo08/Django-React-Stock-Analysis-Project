import requests
from django.core.management.base import BaseCommand
from stock_data.models import Stock, StockPrice

class Command(BaseCommand):
    help = 'Fetch stock data from API'

    def handle(self, *args, **kwargs):
        # Example API call (Alpha Vantage)
        API_KEY = '6N1KQG6J4CUBF4O0'
        STOCK_SYMBOL = 'MSFT'
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK_SYMBOL}&apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        
        stock, created = Stock.objects.get_or_create(symbol=STOCK_SYMBOL, defaults={'name': 'Apple Inc.'})
        time_series = data['Time Series (Daily)']
        
        for date, values in time_series.items():
            StockPrice.objects.update_or_create(
                stock=stock,
                date=date,
                defaults={
                    'open_price': values['1. open'],
                    'close_price': values['4. close'],
                    'high_price': values['2. high'],
                    'low_price': values['3. low'],
                    'volume': values['5. volume']
                }
            )
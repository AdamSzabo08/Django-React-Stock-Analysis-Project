import requests
from django.core.management.base import BaseCommand
from stock_data.models import Stock, StockPrice

class Command(BaseCommand):
    help = 'Fetch stock data from API'

    def add_arguments(self, parser):
        parser.add_argument('symbol', type=str, help='Stock symbol to fetch data for')
        parser.add_argument('name', type=str, help='Name of the stock')

    def handle(self, *args, **kwargs):
        API_KEY = '6N1KQG6J4CUBF4O0'
        STOCK_SYMBOL = kwargs['symbol']
        STOCK_NAME = kwargs['name']
        
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK_SYMBOL}&apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        
        stock, created = Stock.objects.get_or_create(symbol=STOCK_SYMBOL, defaults={'name': STOCK_NAME})
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

        self.stdout.write(self.style.SUCCESS(f'Successfully fetched data for {STOCK_SYMBOL} ({STOCK_NAME})'))

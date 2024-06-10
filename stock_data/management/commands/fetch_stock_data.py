import requests
from django.core.management.base import BaseCommand
from stock_data.models import Stock, StockPrice
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch stock data from API'

    def add_arguments(self, parser):
        parser.add_argument('symbol', type=str, help='Stock symbol to fetch data for')
        parser.add_argument('name', type=str, help='Name of the stock')

    def handle(self, *args, **kwargs):
        API_KEY = '6N1KQG6J4CUBF4O0'
        STOCK_SYMBOL = kwargs['symbol']
        STOCK_NAME = kwargs['name']
        
        logger.debug(f'Start fetching data for {STOCK_SYMBOL} ({STOCK_NAME})')
        
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK_SYMBOL}&apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        
        if "Time Series (Daily)" not in data:
            logger.error(f"Error fetching data for {STOCK_SYMBOL}: {data}")
            self.stdout.write(self.style.ERROR(f'Error fetching data for {STOCK_SYMBOL}'))
            return
        
        stock, created = Stock.objects.get_or_create(symbol=STOCK_SYMBOL, defaults={'name': STOCK_NAME})
        time_series = data['Time Series (Daily)']
        
        if not time_series:
            logger.error(f"No time series data found for {STOCK_SYMBOL}")
            self.stdout.write(self.style.ERROR(f'No time series data found for {STOCK_SYMBOL}'))
            return
        
        for date, values in time_series.items():
            if not all(k in values for k in ('1. open', '2. high', '3. low', '4. close', '5. volume')):
                logger.error(f"Incomplete data for date {date} for {STOCK_SYMBOL}")
                continue
            
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
            logger.debug(f'Updated/created stock price for {STOCK_SYMBOL} on {date}')

        self.stdout.write(self.style.SUCCESS(f'Successfully fetched data for {STOCK_SYMBOL} ({STOCK_NAME})'))
        logger.debug(f'Successfully fetched data for {STOCK_SYMBOL} ({STOCK_NAME})')

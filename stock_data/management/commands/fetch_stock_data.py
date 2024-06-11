import requests
from django.core.management.base import BaseCommand
from stock_data.models import Stock, StockPrice
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch stock data from API'

    def add_arguments(self, parser):
        parser.add_argument('symbol', type=str, help='Stock symbol to fetch data for')

    def handle(self, *args, **kwargs):
        API_KEY = '6N1KQG6J4CUBF4O0'
        STOCK_SYMBOL = kwargs['symbol']

        logger.debug(f'Start fetching data for {STOCK_SYMBOL}')

        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK_SYMBOL}&apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()

        logger.debug(f'Response from Alpha Vantage: {data}')

        if "Time Series (Daily)" not in data:
            logger.error(f"Error fetching data for {STOCK_SYMBOL}: {data}")
            self.stdout.write(self.style.ERROR(f'Error fetching data for {STOCK_SYMBOL}'))
            return

        time_series = data.get('Time Series (Daily)', {})

        if not time_series:
            logger.error(f"No time series data found for {STOCK_SYMBOL}")
            self.stdout.write(self.style.ERROR(f'No time series data found for {STOCK_SYMBOL}'))
            return

        stock, created = Stock.objects.get_or_create(symbol=STOCK_SYMBOL, defaults={'name': ''})

        if created:
            # Fetch stock name from Alpha Vantage
            stock_name_url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={STOCK_SYMBOL}&apikey={API_KEY}'
            response = requests.get(stock_name_url)
            logger.debug(f'Response from Alpha Vantage for stock name: {response.json()}')
            if response.status_code == 200:
                results = response.json().get('bestMatches', [])
                if results:
                    stock.name = results[0].get('2. name')
                    stock.save()

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

        close_prices = [float(values['4. close']) for values in time_series.values() if '4. close' in values]
        if close_prices:
            min_close_price = min(close_prices)
            max_close_price = max(close_prices)
            logger.debug(f'Min close price: {min_close_price}, Max close price: {max_close_price}')
        else:
            logger.error(f"No valid closing prices for {STOCK_SYMBOL}")
            self.stdout.write(self.style.ERROR(f'No valid closing prices for {STOCK_SYMBOL}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Successfully fetched data for {STOCK_SYMBOL}'))
        logger.debug(f'Successfully fetched data for {STOCK_SYMBOL}')

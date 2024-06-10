from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db.models import Avg, Max, Min
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
from .models import Stock, StockPrice
import json
import logging

logger = logging.getLogger(__name__)

def stock_list(request):
    stocks = Stock.objects.all()
    stock_list = [{'id': stock.id, 'name': stock.name, 'symbol': stock.symbol} for stock in stocks]
    return JsonResponse(stock_list, safe=False)

def stock_detail(request, symbol):
    stock = get_object_or_404(Stock, symbol=symbol)
    stock_prices = StockPrice.objects.filter(stock=stock).order_by('-date')
    
    stock_data = {
        'stock': {
            'name': stock.name,
            'symbol': stock.symbol
        },
        'stock_prices': [
            {
                'date': price.date.strftime('%Y-%m-%d'),
                'close_price': price.close_price
            } for price in stock_prices
        ]
    }
    
    return JsonResponse(stock_data)

def stock_analysis(request, symbol):
    stock = get_object_or_404(Stock, symbol=symbol)
    stock_prices = StockPrice.objects.filter(stock=stock)
    analysis = {
        'stock': {'id': stock.id, 'name': stock.name, 'symbol': stock.symbol},
        'average_close': stock_prices.aggregate(Avg('close_price'))['close_price__avg'],
        'highest_close': stock_prices.aggregate(Max('close_price'))['close_price__max'],
        'lowest_close': stock_prices.aggregate(Min('close_price'))['close_price__min'],
        'average_volume': stock_prices.aggregate(Avg('volume'))['volume__avg'],
    }
    return JsonResponse(analysis)

@csrf_exempt
def add_stock(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.debug(f'Received data: {data}')
            symbol = data.get('symbol')
            name = data.get('name')

            if not symbol or not name:
                logger.error('Missing symbol or name')
                return JsonResponse({'error': 'Missing symbol or name'}, status=400)

            stock, created = Stock.objects.get_or_create(symbol=symbol, defaults={'name': name})
            logger.debug(f'Stock created: {created}, Stock: {stock}')

            if created:
                try:
                    logger.debug(f'Calling fetch_stock_data for symbol: {symbol}, name: {name}')
                    call_command('fetch_stock_data', symbol=symbol, name=name)
                    logger.debug(f'Successfully fetched data for {symbol}')
                    return JsonResponse({'message': 'Stock added and data fetched successfully'}, status=201)
                except Exception as e:
                    logger.error(f'Error fetching stock data for {symbol}: {str(e)}')
                    return JsonResponse({'error': f'Error fetching stock data: {str(e)}'}, status=500)
            else:
                logger.error('Stock already exists')
                return JsonResponse({'error': 'Stock already exists'}, status=400)
        except json.JSONDecodeError:
            logger.error('Invalid JSON')
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f'Unexpected error: {str(e)}')
            return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)
    else:
        logger.debug('GET request to add_stock view')
        return HttpResponse("Add Stock View", status=200)

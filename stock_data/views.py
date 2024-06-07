from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Avg, Max, Min, Sum
from .models import Stock, StockPrice

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

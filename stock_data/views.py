from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Max, Min, Sum
from .models import Stock, StockPrice

def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'stock_data/stock_list.html', {'stocks': stocks})

def stock_detail(request, symbol):
    stock = get_object_or_404(Stock, symbol=symbol)
    stock_prices = StockPrice.objects.filter(stock=stock).order_by('-date')
    
    dates = [price.date.strftime('%Y-%m-%d') for price in stock_prices]
    close_prices = [price.close_price for price in stock_prices]
    
    context = {
        'stock': stock,
        'stock_prices': stock_prices,
        'dates': dates,
        'close_prices': close_prices
    }
    
    return render(request, 'stock_data/stock_detail.html', context)

def stock_analysis(request, symbol):
    stock = get_object_or_404(Stock, symbol=symbol)
    stock_prices = StockPrice.objects.filter(stock=stock)
    
    average_close = stock_prices.aggregate(Avg('close_price'))['close_price__avg']
    highest_close = stock_prices.aggregate(Max('close_price'))['close_price__max']
    lowest_close = stock_prices.aggregate(Min('close_price'))['close_price__min']
    average_volume = stock_prices.aggregate(Avg('volume'))['volume__avg']
    
    context = {
        'stock': stock,
        'average_close': average_close,
        'highest_close': highest_close,
        'lowest_close': lowest_close,
        'average_volume': average_volume
    }
    
    return render(request, 'stock_data/stock_analysis.html', context)

from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from .models import Stock, StockPrice

def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'stock_data/stock_list.html', {'stocks': stocks})

def stock_detail(request, symbol):
    stock = get_object_or_404(Stock, symbol=symbol)
    stock_prices = StockPrice.objects.filter(stock=stock).order_by('-date')
    return render(request, 'stock_data/stock_detail.html', {'stock': stock, 'stock_prices': stock_prices})

def stock_analysis(request, symbol):
    stock = get_object_or_404(Stock, symbol=symbol)
    average_close = StockPrice.objects.filter(stock=stock).aggregate(Avg('close_price'))['close_price__avg']
    return render(request, 'stock_data/stock_analysis.html', {'stock': stock, 'average_close': average_close})

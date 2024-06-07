from django.urls import path
from . import views

urlpatterns = [
    path('', views.stock_list, name='stock_list'),
    path('stocks/', views.stock_list, name='stock_list'),
    path('stocks/<str:symbol>/', views.stock_detail, name='stock_detail'),
    path('stocks/<str:symbol>/analysis/', views.stock_analysis, name='stock_analysis'),
]

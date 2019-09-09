from django import forms
from .models import Stock, Shares
from django.db import models
from django.forms import ModelForm
from trading.models import Trading_Account

class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ('stock_name', 'stock_max')

class SharesForm(ModelForm):
    class Meta:
        model = Shares
        fields = ['shares_amount',]

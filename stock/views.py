from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import StockForm, SharesForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from stock.models import Stock, Shares
from trading.models import Trading_Account
# Create your views here.

@login_required(login_url="/users")
def stock_create_view(request, id, *args, **kwargs):
    form = StockForm(request.POST or None)
    if form.is_valid():
        stock = form.save(commit=False)
        stock.trading_id = Trading_Account.objects.get(id=id)
        stock.save()
        form = StockForm()
        return redirect('/trading/' + str(stock.trading_id.id))
    context = {
        'form': form,
        'trading_account': Trading_Account.objects.get(id=id)
    }
    return render(request, 'stock/stock_create.html', context)

@login_required(login_url="/users")
def stock_detail_view(request, id, *args, **kwargs):
    try:
        obj = Stock_Amount.objects.get(id=id)
    except Stock_Amount.DoesNotExist:
        raise Http404
    context = {
        'stock_amount': obj,
    }
    return render(request, 'stock/stock_detail.html', context)

@login_required(login_url="/users")
def stock_list_view(request, *args, **kwargs):
    stock_list = Stock.objects.all().filter(stock_hasValidInfo=True)
    paginator = Paginator(stock_list, 10)
    page = request.GET.get('page')
    try:
        stocks = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        stocks = paginator.page(page)

    #index of the current page
    index = stocks.number - 1
    #maximum index of pages
    max_index = len(paginator.page_range)
    #set range of index to 7
    start_index = index - 3 if index > 3 else 0
    #end_index = index + 3 if index <= max_index - 3 else max_index
    if index <= max_index:
        if index <= 3:
            end_index = 7
        else:
            end_index = index+4
    else:
        end_index = max_index
    page_range = list(paginator.page_range)[start_index:end_index]
    return render(request, 'stock/stock_list.html', {
    'stocks': stocks,
    'page_range':page_range,
    })

@login_required(login_url="/users")
def stock_buy(request, stock_ticker, *args, **kwargs):
    stock = request.GET.get('stock')
    try:
        stock = Stock.objects.get(stock_ticker=stock_ticker)
    except Stock.DoesNotExist:
        raise Http404
    stock_available = stock.stock_max - stock.stock_sold
    user= request.user
    trading_accounts = Trading_Account.objects.filter(user_id=user.id)
    form = SharesForm(request.POST or None)
    if form.is_valid():
    #if request.method =='POST':
        shares = form.save(commit=False)
        #account = document.getElementById("selectedAccount").value
        account = request.POST.get('selectedAccount')
        print(account)
        tradingAccount = Trading_Account.objects.filter(trading_name=account, user_id=user.id)
        print(tradingAccount[0])
        shares.tradingID= tradingAccount[0]
        shares.stockID = stock
        #quantity = request.POST.get('number')
        stock.stock_sold += shares.shares_amount
        shares.save()
        form = SharesForm()
    context = {
        'stock_ticker': stock_ticker,
        'stock_name': stock.stock_name,
        'stock_price' : stock.stock_price,
        'stock_available': stock_available,
        'trading_accounts': trading_accounts,
        'form': form
    }
    return render(request, 'stock/stock_buy.html', context)

@login_required(login_url="/users")
def stock_sell(request, *args, **kwargs):
    return render(request, 'stock/stock_sell.html')

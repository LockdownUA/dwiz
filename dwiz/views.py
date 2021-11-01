from app.models import Profile
from dwiz.forms import LoginForm
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from pythonAPI.dwapi import datawiz
from dwiz.func import (
    get_turnover,
    get_count_receipts,
    get_middle_check,
    get_count_products,
    diff_percent,
    difference,
    get_products,
    get_info_products
)


def main_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    dw = datawiz.DW()

    products = dw.get_products_sale(date_from="2015-11-17", date_to="2015-11-18")
    receipts = dw.get_receipts(date_from="2015-11-17", date_to="2015-11-18")
    
    # Оборот
    turnover1 = get_turnover(products.loc["2015-11-17"])
    turnover2 = get_turnover(products.loc["2015-11-18"])
    diff_percent_turnover = diff_percent(turnover1, turnover2)
    diff_turnover = difference(turnover1, turnover2)

    # Кількість товарів
    count_products1 = get_count_products(receipts, "2015-11-17")
    count_products2 = get_count_products(receipts, "2015-11-18")
    diff_percent_count_prod = diff_percent(count_products1, count_products2)
    diff_count_prod = difference(count_products1, count_products2)

    # Кількість чеків
    count_receipts1 = get_count_receipts(receipts, "2015-11-17")
    count_receipts2 = get_count_receipts(receipts, "2015-11-18")
    diff_percent_count_rec = diff_percent(count_receipts1, count_receipts2)
    diff_count_rec = difference(count_receipts1, count_receipts2)

    # Середні чеки
    mcheck1 = get_middle_check(receipts, "2015-11-17")
    mcheck2 = get_middle_check(receipts, "2015-11-18")
    diff_percent_mcheck = diff_percent(mcheck1, mcheck2)
    diff_mcheck = difference(mcheck1, mcheck2)

    res = []
    res.append(turnover2)
    res.append(turnover1)
    res.append(diff_percent_turnover)
    res.append(diff_turnover)
    res.append(count_products2)
    res.append(count_products1)
    res.append(diff_percent_count_prod)
    res.append(diff_count_prod)
    res.append(count_receipts2)
    res.append(count_receipts1)
    res.append(diff_percent_count_rec)
    res.append(diff_count_rec)
    res.append(mcheck2)
    res.append(mcheck1)
    res.append(diff_percent_mcheck)
    res.append(diff_mcheck)

    context = {
        'res' : res,
    }

    return render(request, 'main/main.html', context)

def top_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    dw = datawiz.DW()

    receipts = dw.get_receipts(date_from="2015-11-17", date_to="2015-11-18")

    prod17 = get_products(receipts, "2015-11-17") # Інфа по товарах за 17 число
    prod18 = get_products(receipts, "2015-11-18") # Інфа по товарах за 18 число

    top = [] # Товари які піднялись в обороті
    down = [] # Товари які зменшились в обороті
    get_info_products(prod17, prod18, top, down)

    paginator = Paginator(sorted(top, key=lambda d: d['total'], reverse=True), 100)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = "?page={}".format(page.previous_page_number())
    else:
        prev_url = ""

    if page.has_next():
        next_url = "?page={}".format(page.next_page_number())
    else:
        next_url = ""

    context = {
        'res' : page,
        'is_paginated' : is_paginated,
        'prev_url' : prev_url,
        'next_url' : next_url,
    }
    return render(request, 'main/top.html', context)

def down_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    dw = datawiz.DW()

    receipts = dw.get_receipts(date_from="2015-11-17", date_to="2015-11-18")

    prod17 = get_products(receipts, "2015-11-17") # Інфа по товарах за 17 число
    prod18 = get_products(receipts, "2015-11-18") # Інфа по товарах за 18 число

    top = [] # Товари які піднялись в обороті
    down = [] # Товари які зменшились в обороті
    get_info_products(prod17, prod18, top, down)

    paginator = Paginator(sorted(down, key=lambda d: d['total']), 100)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = "?page={}".format(page.previous_page_number())
    else:
        prev_url = ""

    if page.has_next():
        next_url = "?page={}".format(page.next_page_number())
    else:
        next_url = ""

    context = {
        'res' : page,
        'is_paginated' : is_paginated,
        'prev_url' : prev_url,
        'next_url' : next_url,
    }
    return render(request, 'main/down.html', context)

def client_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    
    dw = datawiz.DW()

    client = dw.get_client_info()

    shops = []
    for s in client['shops']:
       tmp = client['shops'].get(s)
       shops.append(tmp)

    context = {
        'client' : client,
        'shops' : shops,
    }
    return render(request, 'main/client.html', context)

def login_view(request):
    if request.method == 'GET':
        form = LoginForm(request.POST or None)

        context = {
            'form' : form,
        }
        return render(request, 'main/login.html', context)

    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'main/login.html', {'form' : form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')

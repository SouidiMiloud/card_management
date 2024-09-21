from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, Account, SupportTicket, Shopping, TicketMessage, SelfAccount, HQCard, VHQCard, DumpCard, WholesaleCard, SellingItem, Invoice
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SelfAccountForm, WholesaleCardForm, HQCardForm, VHQCardForm, DumpCardForm, XLSXUploadForm
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
import pandas as pd
from html import unescape

import json
import hashlib
import hmac
import uuid
import requests
from django.conf import settings


@login_required
def add_funds(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')  
        currency = request.POST.get('currency', 'BTC')  
        user_email = request.user.email 

        params = {
            'source_currency': 'USD',
            'source_amount': amount,
            'currency': currency,
            'email': user_email,
            'order_number': str(uuid.uuid4()),  
            'order_name': f'{currency} payment',
            'callback_url': f'{settings.MY_SITE_URL}/callback',  
            'api_key': settings.PLISIO_API_KEY,
            'expire_min': '30',
        }

        response = requests.get(settings.PLISIO_BASE_URL, params=params)
      
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                Invoice.objects.create(
                    user = request.user,
                    order_number=params['order_number'],
                    crypto_amount = float(data['data']['invoice_total_sum']),
                    amount = float(params['source_amount']),
                    currency = params['currency'],
                    address = '',
                    url = data['data']['invoice_url']
                )
                return render(request, 'cards/payment_response.html', {'status': 'success', 'invoice_url': data['data']['invoice_url']})
        return render(request, 'cards/payment_response.html', {'status': 'fail'})
    else:
        invoices = Invoice.objects.filter(user=request.user)
        return render(request, 'cards/add_funds.html', {'invoices': invoices})
    
@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        try:
            data = request.POST

            secret_key = settings.PLISIO_API_KEY  
            data = dict(data)
            
            '''
            if 'verify_hash' not in request.POST:
                return JsonResponse({'status': 'error', 'message': 'verify_hash missing'}, status=400)
            
            post_data = request.POST.copy()
            verify_hash = post_data.pop('verify_hash')[0]  
            
            sorted_post_data = dict(sorted(post_data.items()))
            
            if 'expire_utc' in sorted_post_data:
                sorted_post_data['expire_utc'] = str(sorted_post_data['expire_utc'])
            
            if 'tx_urls' in sorted_post_data:
                sorted_post_data['tx_urls'] = unescape(sorted_post_data['tx_urls'])
            
            post_string = str(sorted_post_data).encode('utf-8')
            
            check_key = hmac.new(secret_key.encode('utf-8'), post_string, hashlib.sha1).hexdigest()
            
            if check_key != verify_hash:
                return JsonResponse({'status': 'error', 'message': 'Invalid hash'}, status=400)
            '''


            order_number = data.get('order_number')[0]
            invoice = Invoice.objects.get(order_number=order_number)
            if data.get('status') == 'completed':
                amount = data.get('amount')
                currency = data.get('currency')

                invoice.status = 'paid'
                invoice.save()
                account = Account.objects.get(user=invoice.user)
                account.balance += int(amount)
                account.save()

                return JsonResponse({"status": "success", "message": "Payment processed"}, status=200)
            elif data.get('status') == 'expired':
                invoice.status = 'expired'
                invoice.save()

                return JsonResponse({"status": "expired", "message": "Transaction expired"}, status=200)
            else:
                invoice.status = 'pending'
                invoice.save()
                return JsonResponse({"status": "pending", "message": "Payment pending"}, status=200)

        except Exception as e:
            print(f'error: {str(e)}')
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@login_required
def home(request):
    '''
    acc = Order.objects.all()
    for a in acc:
        a.delete()
    
    shops = Shopping.objects.all()
    for s in shops:
        s.delete()
    
    ticks = SupportTicket.objects.all()
    for t in ticks:
        t.delete()
    
    msg = TicketMessage.objects.all()
    for m in msg:
        m.delete()
    
    sl = SellingItem.objects.all()
    for s in sl:
        s.delete()
    '''

    '''
    https://doc.cryptomus.com/personal/general/request-format
    api key

    d141906f61e863c1e1fbafee00e1786dce4305f8
    '''




    return render(request, 'cards/home.html', {'username': request.user.username})

@login_required
def hq_detail_cards(request):
    cards = HQCard.objects.filter(available=True)
    countries = list(set(card.country for card in cards))
    bases = list(set(card.base for card in cards))
    zips = list(set(card.card_zip for card in cards))
    banks = list(set(card.bank_name for card in cards))
    states = list(set(card.state for card in cards))
    cities = list(set(card.city for card in cards))
    statuses = list(set(card.status for card in cards))
    credit_debits = list(set(card.credit_debit for card in cards))
    levels = list(set(card.level for card in cards))
    if '?' in request.get_full_path():
        base = request.GET.get('base')
        card_zip = request.GET.get('zip')
        bank = request.GET.get('bank')
        card_bin = request.GET.get('bin')
        state = request.GET.get('state')
        city = request.GET.get('city')
        zip_checked = request.GET.get('zip_checkbox') == 'true'
        phone_checked = request.GET.get('phone') == 'true'
        status = request.GET.get('status')
        credit_debit = request.GET.get('credit_debit')
        level = request.GET.get('level')
        refundable_checked = request.GET.get('refundable') == 'true'
    
        country = request.GET.get('country')
        min_price = request.GET.get('min_price', 0)
        max_price = request.GET.get('max_price', 1000)
        dob_checked = request.GET.get('dob') == 'true'
        ssn_checked = request.GET.get('ssn') == 'true'
        ip_checked = request.GET.get('ip') == 'true'
        email_checked = request.GET.get('email') == 'true'
        address_checked = request.GET.get('address') == 'true'
        ua_checked = request.GET.get('ua') == 'true'

        if status and status != 'All':
            cards = cards.filter(status=status)
        if credit_debit and credit_debit != 'All':
            cards = cards.filter(credit_debit=credit_debit)
        if level and level != 'All':
            cards = cards.filter(level=level)
        if card_bin != '':
            cards = cards.filter(card_bin=card_bin)
        if base and base != 'All':
            cards = cards.filter(base=base)
        if bank and bank != 'All':
            cards = cards.filter(bank_name=bank)
        if card_zip and card_zip != 'All':
            cards = cards.filter(card_zip=card_zip)
        if state and state != 'All':
            cards = cards.filter(state=state)
        if city and city != 'All':
            cards = cards.filter(city=city)
        if country and country != 'All':
            cards = cards.filter(country=country)
        cards = cards.filter(price__gte=min_price, price__lte=max_price)
        if ssn_checked:
            cards = cards.filter(ssn__isnull=False)
        if ip_checked:
            cards = cards.filter(ip__isnull=False)
        if dob_checked:
            cards = cards.filter(dob__isnull=False)
        if email_checked:
            cards = cards.filter(email__isnull=False)
        if refundable_checked:
            cards = cards.filter(refundable=True)
        if zip_checked:
            cards = cards.filter(card_zip__isnull=False)
        if phone_checked:
            cards = cards.filter(phone__isnull=False)
        if address_checked:
            cards = cards.filter(address__isnull=False)
        if ua_checked:
            cards = cards.filter(ua__isnull=False)
    return render(request, 'cards/hq_detail_cards.html', {
        'cards': cards,
        'countries': countries,
        'bases': bases,
        'zips': zips,
        'banks': banks,
        'states': states,
        'cities': cities,
        'statuses': statuses,
        'credit_debits': credit_debits,
        'levels': levels
    })

@login_required
def vhq_detail_cards(request):
    cards = VHQCard.objects.filter(available=True)
    countries = list(set(card.country for card in cards))
    bases = list(set(card.base for card in cards))
    banks = list(set(card.bank_name for card in cards))
    cities = list(set(card.city for card in cards))
    statuses = list(set(card.status for card in cards))
    levels = list(set(card.level for card in cards))
    if '?' in request.get_full_path():
        base = request.GET.get('base')
        bank = request.GET.get('bank')
        card_bin = request.GET.get('bin')
        city = request.GET.get('city')
        phone_checked = request.GET.get('phone') == 'true'
        status = request.GET.get('status')
        level = request.GET.get('level')
        refundable_checked = request.GET.get('refundable') == 'true'
    
        country = request.GET.get('country')
        min_price = request.GET.get('min_price', 0)
        max_price = request.GET.get('max_price', 1000)
        ip_checked = request.GET.get('ip') == 'true'
        email_checked = request.GET.get('email') == 'true'
        address_checked = request.GET.get('address') == 'true'

        if status and status != 'All':
            cards = cards.filter(status=status)
        if level and level != 'All':
            cards = cards.filter(level=level)
        if card_bin != '':
            cards = cards.filter(card_bin=card_bin)
        if base and base != 'All':
            cards = cards.filter(base=base)
        if bank and bank != 'All':
            cards = cards.filter(bank_name=bank)
        if city and city != 'All':
            cards = cards.filter(city=city)
        if country and country != 'All':
            cards = cards.filter(country=country)
        cards = cards.filter(price__gte=min_price, price__lte=max_price)
        if ip_checked:
            cards = cards.filter(ip__isnull=False)
        if email_checked:
            cards = cards.filter(email__isnull=False)
        if refundable_checked:
            cards = cards.filter(refundable=True)
        if phone_checked:
            cards = cards.filter(phone__isnull=False)
        if address_checked:
            cards = cards.filter(address__isnull=False)
    return render(request, 'cards/vhq_detail_cards.html', {
        'cards': cards,
        'countries': countries,
        'bases': bases,
        'banks': banks,
        'cities': cities,
        'statuses': statuses,
        'levels': levels
    })

@login_required
def dump_detail_cards(request):
    cards = DumpCard.objects.filter(available=True)
    countries = list(set(card.country for card in cards))
    bases = list(set(card.base for card in cards))
    zips = list(set(card.card_zip for card in cards))
    banks = list(set(card.bank_name for card in cards))
    states = list(set(card.state for card in cards))
    cities = list(set(card.city for card in cards))
    statuses = list(set(card.status for card in cards))
    credit_debits = list(set(card.credit_debit for card in cards))
    levels = list(set(card.level for card in cards))
    if '?' in request.get_full_path():
        base = request.GET.get('base')
        card_zip = request.GET.get('zip')
        bank = request.GET.get('bank')
        card_bin = request.GET.get('bin')
        state = request.GET.get('state')
        status = request.GET.get('status')
        credit_debit = request.GET.get('credit_debit')
        level = request.GET.get('level')
    
        country = request.GET.get('country')
        min_price = request.GET.get('min_price', 0)
        max_price = request.GET.get('max_price', 1000)

        if status and status != 'All':
            cards = cards.filter(status=status)
        if credit_debit and credit_debit != 'All':
            cards = cards.filter(credit_debit=credit_debit)
        if level and level != 'All':
            cards = cards.filter(level=level)
        if card_bin != '':
            cards = cards.filter(card_bin=card_bin)
        if base and base != 'All':
            cards = cards.filter(base=base)
        if bank and bank != 'All':
            cards = cards.filter(bank_name=bank)
        if card_zip and card_zip != 'All':
            cards = cards.filter(card_zip=card_zip)
        if state and state != 'All':
            cards = cards.filter(state=state)
        if country and country != 'All':
            cards = cards.filter(country=country)
        cards = cards.filter(price__gte=min_price, price__lte=max_price)

    return render(request, 'cards/dump_detail_cards.html', {
        'cards': cards,
        'countries': countries,
        'bases': bases,
        'zips': zips,
        'banks': banks,
        'states': states,
        'cities': cities,
        'statuses': statuses,
        'credit_debits': credit_debits,
        'levels': levels
    })

@login_required
def wholesale_detail_cards(request):
    cards = WholesaleCard.objects.filter(available=True)
    countries = list(set(card.country for card in cards))
    if '?' in request.get_full_path():
        country = request.GET.get('country')
        min_price = request.GET.get('min_price', 0)
        max_price = request.GET.get('max_price', 1000)
        address_checked = request.GET.get('address') == 'true'
        dob_checked = request.GET.get('dob') == 'true'
        email_checked = request.GET.get('email') == 'true'
        if country and country != 'All':
            cards = cards.filter(country=country)
        cards = cards.filter(price__gte=min_price, price__lte=max_price)
        if address_checked:
            cards = cards.filter(address__isnull=False)
        if dob_checked:
            cards = cards.filter(dob__isnull=False)
        if email_checked:
            cards = cards.filter(email__isnull=False)
    return render(request, 'cards/wholesale_detail_cards.html', {
        'cards': cards,
        'countries': countries
    })

@login_required
def self_account_detail_cards(request):
    self_accounts = SelfAccount.objects.filter(available=True)
    countries = list(set(card.country for card in self_accounts))
    account_types = list(set(self_account.account_type for self_account in self_accounts))
    if '?' in request.get_full_path():
        account_type = request.GET.get('account_type')
        country = request.GET.get('country')
        min_price = request.GET.get('min_price', 0)
        max_price = request.GET.get('max_price', 1000)
        
        if country and country != 'All':
            self_accounts = self_accounts.filter(country=country)
        if account_type and account_type != 'All':
            self_accounts = self_accounts.filter(account_type=account_type)            
        self_accounts = self_accounts.filter(price__gte=min_price, price__lte=max_price)

    return render(request, 'cards/self_account_list.html', {
        'self_accounts': self_accounts,
        'countries': countries,
        'account_types': account_types,
    })

def proof(request, account_id):
    self_account = SelfAccount.objects.get(id=account_id)
    return render(request, 'cards/proof.html', {'self_account': self_account})

def buy_card(request, shopping):
    item = shopping.item
    item.available = False
    item.save()
    Order.objects.create(user=request.user, item=item, price=item.price, item_type=shopping.item_type)

@login_required
def buy(request):
    shoppings = Shopping.objects.filter(user=request.user)
    total = total_shoppings_price(request.user)
    account = Account.objects.get(user=request.user)
    if account.balance >= total:
        account.balance -= total
        account.save()
        for shopping in shoppings:
            buy_card(request, shopping)
        for shopping in shoppings:
            shopping.delete()
        return redirect('home')
    else:
        return render(request, 'cards/insufficient_balance.html')

@login_required
def hq_orders(request):
    orders = Order.objects.filter(user=request.user, item_type='HQCard')
        
    order_items = []
    for order in orders:
        order_items.append({
            'order': order,
            'item': HQCard.objects.get(pk=order.item.id)
        })
    return render(request, 'cards/orders.html', {'order_items': order_items, 'orders_type': 'HQCard'})

@login_required
def vhq_orders(request):
    orders = Order.objects.filter(user=request.user, item_type='VHQCard')
    order_items = []
    for order in orders:
        order_items.append({
            'order': order,
            'item': VHQCard.objects.get(pk=order.item.id)
        })
    return render(request, 'cards/orders.html', {'order_items': order_items, 'orders_type': 'VHQCard'})

@login_required
def dump_orders(request):
    orders = Order.objects.filter(user=request.user, item_type='DumpCard')
    order_items = []
    for order in orders:
        order_items.append({
            'order': order,
            'item': DumpCard.objects.get(pk=order.item.id)
        })
    return render(request, 'cards/orders.html', {'order_items': order_items, 'orders_type': 'DumpCard'})

@login_required
def wholesale_orders(request):
    orders = Order.objects.filter(user=request.user, item_type='WholesaleCard')
    order_items = []
    for order in orders:
        order_items.append({
            'order': order,
            'item': WholesaleCard.objects.get(pk=order.item.id)
        })
    return render(request, 'cards/orders.html', {'order_items': order_items, 'orders_type': 'WholesaleCard'})

@login_required
def self_account_orders(request):
    orders = Order.objects.filter(user=request.user, item_type='SelfAccount')
    order_items = []
    for order in orders:
        order_items.append({
            'order': order,
            'item': SelfAccount.objects.get(pk=order.item.id)
        })
    return render(request, 'cards/orders.html', {'order_items': order_items, 'orders_type': 'SelfAccount'})


@login_required
def support_tickets(request):
    if request.user.is_superuser:
        tickets = SupportTicket.objects.all()
    else:
        tickets = SupportTicket.objects.filter(user=request.user)
    return render(request, 'cards/support_tickets.html', {'tickets': tickets})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            user = User.objects.create_user(username, email, password)

            Account.objects.create(user=user)

            return JsonResponse({'success': True, 'message': 'Registration successful'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
    return render(request, 'cards/register.html')

def user_login(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        payload = json.loads(data)
        username = payload.get('username')
        password = payload.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'success': False, 'message': 'Invalid username or password'}, status=400)
    return render(request, 'cards/login.html')

def authenticate_user(request):
    return render(request, 'cards/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def add_hq_card(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        form = HQCardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hq_detail_cards') 
    else:
        form = HQCardForm()
    return render(request, 'cards/add_card.html', {'form': form})

@login_required
def add_vhq_card(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        form = VHQCardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vhq_detail_cards')  
    else:
        form = VHQCardForm()
    return render(request, 'cards/add_card.html', {'form': form})

@login_required
def add_dump_card(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        form = DumpCardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dump_detail_cards')  
    else:
        form = DumpCardForm()
    return render(request, 'cards/add_card.html', {'form': form})

@login_required
def add_wholesale_card(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        form = WholesaleCardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wholesale_detail_cards')  
    else:
        form = WholesaleCardForm()
    return render(request, 'cards/add_card.html', {'form': form})

@login_required
def add_self_account(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        form = SelfAccountForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()  
            return redirect('self_account_detail_cards')  
    else:
        form = SelfAccountForm()
    return render(request, 'cards/add_self_account.html', {'form': form})


def get_shopping_items(user):
    shoppings = Shopping.objects.filter(user=user)
    shopping_items = []
    for shopping in shoppings:
        specific_item = get_specific_item(shopping.item_type, shopping.item.id)
        print(type(specific_item).__name__)
        
        shopping_items.append({
            'shopping': shopping,
            'specific_item': specific_item,
            'item_type': type(specific_item).__name__
        })
    return shopping_items

@login_required
def shoppings(request):
    
    shopping_items = get_shopping_items(request.user)
    total = total_shoppings_price(request.user)
    return render(request, 'cards/shoppings.html', {'shopping_items': shopping_items, 'total': total})


@login_required
def add_hq_shop(request, card_id):
    card = HQCard.objects.get(id=card_id)
    Shopping.objects.create(user=request.user, item=card, item_type='HQCard')
    total = total_shoppings_price(request.user)
    shopping_items = get_shopping_items(request.user)
    return render(request, 'cards/shoppings.html', {'shopping_items': shopping_items, 'total': total})

@login_required
def add_vhq_shop(request, card_id):
    card = VHQCard.objects.get(id=card_id)
    Shopping.objects.create(user=request.user, item=card, item_type='VHQCard')
    total = total_shoppings_price(request.user)
    shopping_items = get_shopping_items(request.user)
    return render(request, 'cards/shoppings.html', {'shopping_items': shopping_items, 'total': total})

@login_required
def add_dump_shop(request, card_id):
    card = DumpCard.objects.get(id=card_id)
    Shopping.objects.create(user=request.user, item=card, item_type='DumpCard')
    total = total_shoppings_price(request.user)
    shopping_items = get_shopping_items(request.user)
    return render(request, 'cards/shoppings.html', {'shopping_items': shopping_items, 'total': total})

@login_required
def add_wholesale_shop(request, card_id):
    card = WholesaleCard.objects.get(id=card_id)
    Shopping.objects.create(user=request.user, item=card, item_type='WholesaleCard')
    total = total_shoppings_price(request.user)
    shopping_items = get_shopping_items(request.user)
    return render(request, 'cards/shoppings.html', {'shopping_items': shopping_items, 'total': total})

@login_required
def add_self_account_shop(request, account_id):
    account = SelfAccount.objects.get(id=account_id)
    if not Shopping.objects.filter(item=account).exists():
        Shopping.objects.create(user=request.user, item=account, item_type='SelfAccount')
    total = total_shoppings_price(request.user)
    shopping_items = get_shopping_items(request.user)
    return render(request, 'cards/shoppings.html', {'shopping_items': shopping_items, 'total': total})

def total_shoppings_price(user):
    shoppings = Shopping.objects.filter(user=user)
    total = 0
    for shopping in shoppings:
        total += shopping.item.price
    return total

@login_required
def remove_shopping(request, shopping_id):
    shopping = Shopping.objects.get(id=shopping_id)
    shopping.delete()
    return redirect(shoppings)

@login_required
def profile(request):
    user = request.user
    return render(request, 'cards/profile.html', {'user': user})

@login_required
def update_password(request):
    if request.method == 'POST':
        old_password = request.POST['current_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        if not request.user.check_password(old_password):
            messages.error(request, 'Your current password is incorrect.')
        elif new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
        else:
            request.user.set_password(new_password1)
            request.user.save()
            update_session_auth_hash(request, request.user)  
            messages.success(request, 'Your password has been successfully changed.')
            return redirect('profile')
    return redirect('profile')

@login_required
def new_ticket(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        ticket = SupportTicket.objects.create(user=request.user, subject=subject)
        TicketMessage.objects.create(ticket=ticket, sender=request.user, message=message)
        return redirect('ticket_details', ticket_id=ticket.id)
    return render(request, 'cards/new_ticket.html')

@login_required
def ticket_details(request, ticket_id):
    ticket = SupportTicket.objects.get(id=ticket_id)
    ticket_messages = TicketMessage.objects.filter(ticket=ticket)
    return render(request, 'cards/ticket_details.html', {'ticket_messages': ticket_messages, 'ticket': ticket})

@login_required
def reply(request, ticket_id):
    if request.method == 'POST':
        message = request.POST.get('message_content')
        ticket = SupportTicket.objects.get(id=ticket_id)
        TicketMessage.objects.create(ticket=ticket, sender=request.user, message=message)
        ticket.updated_at = timezone.now()
        if ticket.status == 'started':
            ticket.status = 'in_progress'
        ticket.save()
        return redirect('ticket_details', ticket_id=ticket_id)
    
@login_required
def close_ticket(request, ticket_id):
    if request.user.is_superuser:
        ticket = SupportTicket.objects.get(id=ticket_id)
        ticket.status = 'closed'
        ticket.save()
    return redirect('support_tickets')


def get_specific_item(item_type, pk):
    if item_type == 'SelfAccount':
        return SelfAccount.objects.get(pk=pk)
    if item_type == 'HQCard':
        return HQCard.objects.get(pk=pk)
    if item_type == 'VHQCard':
        return VHQCard.objects.get(pk=pk)
    if item_type == 'DumpCard':
        return DumpCard.objects.get(pk=pk)
    return WholesaleCard.objects.get(pk=pk)




def process_xlsx_file(file, model_class, fields):
    if file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
    elif file.name.endswith('.csv'):
        try:
            df = pd.read_csv(file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file, encoding='ISO-8859-1')
    else:
        raise ValueError("Unsupported file type: only .xlsx and .csv are allowed.")
    
    for _, row in df.iterrows():
        data = row.to_dict()
        filtered_data = {key: data.get(key) for key in fields if key in data}
        model_class.objects.create(**filtered_data)

@login_required
def bulk_self_account(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = XLSXUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data['file']
                fields = ['country', 'description', 'price', 'account_type', 'account_url', 'proof', 'username', 'password']
                process_xlsx_file(file, SelfAccount, fields)
                return redirect('home')
        else:
            form = XLSXUploadForm()
        return render(request, 'upload_form.html', {'form': form})

@login_required
def bulk_hq_card(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = XLSXUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data['file']
                fields = ['country', 'description', 'price', 'exp_date', 'name', 'address', 'city', 'state', 'email', 'phone', 'dob', 'ssn', 'ip', 'bank_name', 'base', 'card_bin', 'status', 'level', 'credit_debit', 'card_zip', 'ua', 'refundable']
                process_xlsx_file(file, HQCard, fields)
                return redirect('home')
        else:
            form = XLSXUploadForm()
        return render(request, 'upload_form.html', {'form': form})

@login_required
def bulk_vhq_card(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = XLSXUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data['file']
                fields = ['country', 'description', 'price', 'exp_date', 'name', 'address', 'city', 'state', 'email', 'phone', 'dob', 'ssn', 'ip', 'bank_name', 'base', 'card_bin', 'status', 'level', 'credit_debit', 'card_zip', 'ua', 'refundable', 'months_left', 'screen_resolution', 'user_agent']
                process_xlsx_file(file, VHQCard, fields)
                return redirect('home')
        else:
            form = XLSXUploadForm()
        return render(request, 'upload_form.html', {'form': form})

@login_required
def bulk_wholesale_card(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = XLSXUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data['file']
                fields = ['country', 'description', 'price', 'exp_date', 'name', 'address', 'city', 'state', 'email', 'phone', 'dob', 'ssn', 'ip', 'number', 'quantity', 'user_agents', 'cvv']
                process_xlsx_file(file, WholesaleCard, fields)
                return redirect('home')
        else:
            form = XLSXUploadForm()
        return render(request, 'upload_form.html', {'form': form})

@login_required
def bulk_dump_card(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = XLSXUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data['file']
                fields = ['country', 'description', 'price', 'exp_date', 'name', 'address', 'city', 'state', 'email', 'phone', 'dob', 'ssn', 'ip', 'bank_name', 'base', 'card_bin', 'status', 'level', 'credit_debit', 'card_zip', 'ua', 'refundable', 'track1', 'track2']
                process_xlsx_file(file, DumpCard, fields)
                return redirect('home')
        else:
            form = XLSXUploadForm()
        return render(request, 'upload_form.html', {'form': form})
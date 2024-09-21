from .models import Account, Shopping

def add_balance_to_context(request):
    balance = 0
    shopping_count = 0
    if request.user.is_authenticated:
        try:
            account = Account.objects.get(user=request.user) 
            balance = account.balance

            shopping_count = Shopping.objects.filter(user=request.user).count()
        except Account.DoesNotExist:
            balance = 0
            shopping_count = 0


    return {
        'balance': balance,
        'shopping_count': shopping_count
    }

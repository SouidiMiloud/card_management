from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class SellingItem(models.Model):
    country = CountryField(blank_label='(Select Country)', null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        abstract = False


class SelfAccount(SellingItem):
    account_type = models.CharField(max_length=255)
    account_url = models.CharField(max_length=255)
    proof = models.ImageField(upload_to='cards/static/images/')
    add_date = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.account_url}'  
    

class Card(SellingItem):
    exp_date = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    ssn = models.CharField(max_length=200, blank=True, null=True)
    ip = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        abstract = False
    
    def __str__(self):
        return f'{self.name}'

class HQCard(Card):
    TYPE_CHOICES = [
        ('visa', 'Visa'),
        ('master_card', 'Master Card')
    ]

    LEVEL_CHOICES = [
        ('standard', 'STANDARD'),
        ('gold', 'GOLD'),
        ('classic', 'CLASSIC'),
        ('prepaid', 'PREPAID'),
        ('infinite', 'INFINITE')
    ]

    CREDIT_DEBIT = [
        ('credit', 'CREDIT'),
        ('debit', 'DEBIT')
    ]

    bank_name = models.CharField(max_length=200, null=True, blank=True)
    base = models.CharField(max_length=200)
    card_bin = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=TYPE_CHOICES, default='visa')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='standard')
    credit_debit = models.CharField(max_length=10, choices=CREDIT_DEBIT, default='credit')
    card_zip = models.CharField(max_length=20, null=True, blank=True)
    ua = models.CharField(max_length=200, null=True, blank=True)
    refundable = models.BooleanField(default=True)

    class Meta:
        abstract = False


class VHQCard(HQCard):
    months_left = models.IntegerField()
    screen_resolution = models.CharField(max_length=200, null=True, blank=True)
    user_agent = models.TextField()


class WholesaleCard(Card):
    number = models.CharField(max_length=16)
    quantity = models.IntegerField()
    user_agents = models.TextField()
    cvv = models.CharField(max_length=3)


class DumpCard(HQCard):
    track1 = models.CharField(max_length=10, blank=True, null=True)
    track2 = models.CharField(max_length=10, null=True, blank=True)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(SellingItem, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    item_type = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'


class Shopping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(SellingItem, on_delete=models.CASCADE) 
    item_type = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return f'Shopping {self.id} by {self.user.username}'


class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('started', 'Started'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='started')

    def __str__(self):
        return f'Ticket {self.id} - {self.subject}'


class TicketMessage(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message {self.id} on Ticket {self.ticket.id}'


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('check', 'Check'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('expired', 'Expired'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=128, unique=True)
    crypto_amount = models.DecimalField(max_digits=20, decimal_places=15, default=0.00)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    address = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='check')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Invoice {self.order_number} - {self.status}"
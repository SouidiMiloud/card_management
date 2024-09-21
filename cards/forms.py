from django import forms
from .models import SelfAccount, HQCard, VHQCard, WholesaleCard, DumpCard


class XLSXUploadForm(forms.Form):
    file = forms.FileField(label='Select an .xlsx file')

class SelfAccountForm(forms.ModelForm):
    class Meta:
        model = SelfAccount
        fields = [
            'country', 'description', 'price',
            'account_type', 'account_url', 'proof', 'username', 'password'
        ]

class HQCardForm(forms.ModelForm):
    class Meta:
        model = HQCard
        fields = [
            'country', 'description', 'price',
            'exp_date', 'address', 'city', 'state', 'email', 'phone',
            'dob', 'ssn', 'ip', 'bank_name', 'base', 'card_bin', 'status',
            'level', 'credit_debit', 'card_zip', 'ua', 'refundable'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

class VHQCardForm(forms.ModelForm):
    class Meta:
        model = VHQCard
        fields = [
            'country', 'description', 'price',
            'exp_date', 'address', 'city', 'state', 'email', 'phone',
            'dob', 'ssn', 'ip', 'bank_name', 'base', 'card_bin', 'status',
            'level', 'credit_debit', 'card_zip', 'ua', 'refundable',
            'months_left', 'screen_resolution', 'user_agent'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

class WholesaleCardForm(forms.ModelForm):
    class Meta:
        model = WholesaleCard
        fields = [
            'country', 'description', 'price',
            'exp_date', 'name', 'address', 'city', 'state', 'email', 'phone',
            'dob', 'ssn', 'ip', 'number', 'quantity', 'user_agents', 'cvv'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

class DumpCardForm(forms.ModelForm):
    class Meta:
        model = DumpCard
        fields = [
            'country', 'description', 'price',
            'exp_date', 'name', 'address', 'city', 'state', 'email', 'phone',
            'dob', 'ssn', 'ip', 'bank_name', 'base', 'card_bin', 'status',
            'level', 'credit_debit', 'card_zip', 'ua', 'refundable',
            'track1', 'track2'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
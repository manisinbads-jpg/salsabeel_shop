from django import forms
from .models import Order


class ReceiptUploadForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['receipt']

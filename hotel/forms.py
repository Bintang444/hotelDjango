# forms.py
from django import forms
from .models import Booking

class BuktiPembayaranForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['bukti_pembayaran', 'metode_pembayaran']
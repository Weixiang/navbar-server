# forms.py
from django import forms

class RFIDQueryForm(forms.Form):
    rfid = forms.CharField(label='RFID', max_length=100)

class DataForm(forms.Form):
    data = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), label='Data')
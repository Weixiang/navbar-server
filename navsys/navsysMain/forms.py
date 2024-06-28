# forms.py
from django import forms

class RFIDQueryForm(forms.Form):
    rfid = forms.CharField(label='RFID', max_length=100)

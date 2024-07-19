from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name= forms.CharField(label="", max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}))
    shipping_email= forms.CharField(label="", max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'email'}))
    shipping_phone= forms.CharField(label="", max_length=20, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}))
    shipping_address1 = forms.CharField(label="", max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address Line 1'}))
    shipping_address2 = forms.CharField(label="", max_length=255, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address Line 2'}))
    shipping_city = forms.CharField(label="", max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}))
    shipping_state = forms.CharField(label="", max_length=255, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}))
    shipping_zipcode = forms.CharField(label="", max_length=20, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip Code'}))
    shipping_country = forms.CharField(label="", max_length=255, required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}))
   
    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_phone', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country',]
        exclude = ['user',]
from django import forms

class AdForm(forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=100)
    price = forms.IntegerField()
    phone = forms.CharField(max_length=12)
    

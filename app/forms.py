from django import forms
from .models import Product,Order

# forms.Form
# forms.ModelForm



class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()
   


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('product',)
from django import forms
from .models import Product

# forms.Form
# forms.ModelForm



class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()
   


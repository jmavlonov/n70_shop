from django import forms
from .models import Product,Order,Comment

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
        
        
        
    
class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('product',)
        
        
class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
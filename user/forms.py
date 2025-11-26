from django import forms
from .models import CustomUser


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    
    
    
class RegisterForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = CustomUser
        fields = ['email','password','confirm_password']
        
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if CustomUser.objects.filter(email = email).exists():
            raise forms.ValidationError(f"{email} already exists!")
    
        return email


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Password did not match')
        
        return cleaned_data
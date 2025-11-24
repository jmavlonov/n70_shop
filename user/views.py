from django.shortcuts import render,redirect
from .forms import LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.


def login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data 
            email = cd['email']
            password = cd['password']
            
            user = authenticate(
                request=request,
                email = email,
                password = password
            )
            
            if user is not None:
                if user.is_active:
                    login(request,user)
                    
                    return redirect('app:index')
                
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Username or password is wrong'
                )
                
            
    else:
        form = LoginForm()
        
    context = {
        'form':form
    }
    return render(request,'user/login.html')


def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('app:index')
    
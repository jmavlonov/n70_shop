from django.shortcuts import render ,redirect
from .models import Category , Product
from django.http import JsonResponse
from app.forms import ProductModelForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request,category_id = None):
    
    categories = Category.objects.all()
    
    if category_id:
        products = Product.objects.filter(category = category_id)
    else:
        products = Product.objects.all()
    
    
    context = {
        'categories':categories,
        'products':products
    }
    return render(request,'app/home.html',context)



def detail(request,product_id):
    product = Product.objects.get(id = product_id)
    if not product:
        return JsonResponse(data={'message':'Oops. Page Not Found','status_code':404})
    
    context = {
        'product' : product
    }
    return render(request,'app/detail.html',context)



# name = request.POST.get('name')



@login_required(login_url='/admin/')
def create_product(request):
    if request.method == 'POST':
        form = ProductModelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Product successfully created ✅"
            )
            # add messages
            
            return redirect('app:create')
    else:
        form = ProductModelForm()
        
                
    context = {
        'form':form
    }
    return render(request,'app/create.html',context)


def delete_product(request,pk):
    product = Product.objects.get(id = pk)
    if product:
        product.delete()
        return redirect('app:index')    
    
    return render(request,'app/detail.html')



def update_product(request,pk):
    pass
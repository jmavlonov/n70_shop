from django.shortcuts import render ,redirect
from .models import Category , Product
from django.http import JsonResponse
from app.forms import ProductModelForm
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


def create_product(request):
    
    if request.method == 'POST':
        form = ProductModelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('app:index')
        
    else:
        form = ProductModelForm()
        
        
    context = {
        'form':form
    }
    return render(request,'app/create.html',context)



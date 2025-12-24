from django.shortcuts import render ,redirect
from .models import Category , Product,Comment
from django.http import JsonResponse
from app.forms import ProductModelForm,OrderModelForm,CommentModelForm,ContactForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from app.utils import filter_by_price
from django.db.models import Avg
from django.db.models.functions import Round
from django.core.mail import EmailMessage
from config.settings import DEFAULT_FROM_EMAIL
from django.views.generic import CreateView



def index(request,category_id = None):
    search_query = request.GET.get('q','')
    filter_type = request.GET.get('filter_type','')
    
    categories = Category.objects.all() # 'select * from all'
    
    if category_id:
        products = Product.objects.filter(category = category_id)
    else:
        products = Product.objects.all()
        
    if search_query:
        products = products.filter(Q(name__icontains = search_query) | Q(description__icontains=search_query))

    products = filter_by_price(filter_type,products)
    
    
    
    context = {
        'categories':categories,
        'products':products.annotate(avg_rating = Round(Avg('comments__rating')))
    }
    return render(request,'app/home.html',context)



def detail(request,product_id):
    product = Product.objects.get(id = product_id)
    related_products = Product.objects.filter(category = product.category).exclude(id=product_id)
    comments = product.comments.filter(is_handle=False)
    if not product:
        return JsonResponse(data={'message':'Oops. Page Not Found','status_code':404})
    
    context = {
        'product' : product,
        'comments':comments,
        'related_products':related_products
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
    product = get_object_or_404(Product,pk=pk)
    if request.method == 'POST':
        form = ProductModelForm(request.POST,request.FILES,instance=product)

        if form.is_valid():
            form.save()
            return redirect('app:detail',pk)
    else:
        form = ProductModelForm(instance=product)
        
    context = {
        'form':form,
        'product':product
    }
    return render(request,'app/update.html',context)




def create_order(request,pk):
    product = get_object_or_404(Product,pk=pk)

    if request.method == 'POST':
        print('Order Post sending ....')
        form = OrderModelForm(request.POST)
        if form.is_valid():
            print('form valid')
            order = form.save(commit=False)
            order.product = product
            if order.quantity > product.stock:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Dont enough quantity'
                ) 
            else:
                product.stock -= order.quantity 
                print('order valid ')
                product.save()
                order.save()
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Order successfully sent✅'
                ) 
                return redirect('app:detail',pk)
    else:
        form = OrderModelForm()

    context = {
        'form':form,
        'product':product
    }

    return render(request,'app/detail.html',context)


# Product.objects.create()


def create_comment(request,product_id):
    product = get_object_or_404(Product,pk = product_id)
    if request.method == 'POST':
        form = CommentModelForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('app:detail',product_id)
    else:
        form = CommentModelForm()
        
    context = {
        'form':form,
        'product':product
    }
    return render(request,'app/detail.html',context)

class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentModelForm
    template_name = 'app/detail.html'
    

    # product obyektini olish
    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=kwargs['product_id'])
        return super().dispatch(request, *args, **kwargs)

    # commentni productga bog‘lab saqlash
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.product = self.product
        comment.save()
        return redirect('app:detail', self.product.id)
    
    # def form_invalid(self, form):
    #     response = super().form_invalid(form)
    #     return response
    

    # templatega qo‘shimcha context uzatish
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.product
        return context
        
        
def contact_view(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            
            
            subject = f"New message from: {name}"
            html_content = f"""
            <h3>New Contact Message</h3>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Message:</strong><br>{message}</p>
            """
            
                        
            email = EmailMessage(
                subject=subject,
                body=html_content,
                from_email='Portfolio Contact <onboarding@resend.dev>',
                to=[DEFAULT_FROM_EMAIL],
                reply_to =  [email],
            )
            email.content_subtype = 'html'
            email.send()
            return redirect('app:index')
        
    return render(request,'app/contact.html',{'form':form})
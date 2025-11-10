
from django.urls import path,include
from .views import index,detail,create_product,delete_product

app_name = 'app'

urlpatterns = [
    path('',index,name='index'),
    path('category/<int:category_id>',index,name='products_of_category'),
    path('detail/<product_id>',detail,name='detail'),
    path('create/',create_product,name='create'),
    path('delete/<int:pk>',delete_product,name='delete')
]


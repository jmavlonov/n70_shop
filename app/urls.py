
from django.urls import path,include
from .views import index,detail,create_product,delete_product,update_product,create_order,create_comment,contact_view

app_name = 'app'

urlpatterns = [
    path('',index,name='index'),
    path('category/<int:category_id>',index,name='products_of_category'),
    path('detail/<int:product_id>',detail,name='detail'),
    path('create/',create_product,name='create'),
    path('delete/<int:pk>',delete_product,name='delete'),
    path('update/<int:pk>',update_product,name='update'),
    path('detail/<int:pk>/orders/',create_order,name='create_order'),
    path('detail/<int:product_id>/comments',create_comment,name='create_comment'),
    path('contact/',contact_view,name='contact_view'),
]


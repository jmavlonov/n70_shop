from django.contrib import admin
from .models import Category , Product,Order,Comment
from django.utils.html import format_html
from django.templatetags.static import static
from import_export.admin import ImportExportModelAdmin
from adminsortable2.admin import SortableAdminMixin
from django.urls import reverse



# Register your models here.


admin.site.register(Order)



class ProductInline(admin.StackedInline):
    model = Product
    extra = 2




@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ['id','title','get_products']
    
    inlines = [
        ProductInline,
    ]
    
    def get_products(self,obj):
        return obj.products.count()
    
    get_products.short_description = 'All Products'




@admin.register(Product)
class ProductAdmin(SortableAdminMixin,admin.ModelAdmin):
    list_display = ['name','price','category','is_stock','get_image']
    list_filter = ['category','updated_at']
    search_fields = ['name',]
    
    def get_image(self,obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" />'.format(obj.image.url))
        
        return format_html('<img src="{}" width="80" height="80" />'.format(static('app/images/not_found_image.avif')))
    
    get_image.short_description = 'Is Stock'

    
    
    def is_stock(self,obj):
        return obj.stock > 0
    
    is_stock.boolean = True



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','rating','is_handle','product__id']
    list_editable = ("is_handle",)

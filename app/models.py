from django.db import models
from decimal import Decimal
from django.templatetags.static import static



# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Categories'


# DRF => Don't repeat yourself

class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    price = models.DecimalField(max_digits=14,decimal_places=2)
    image = models.ImageField(upload_to='products/',null=True,blank=True)
    stock = models.PositiveSmallIntegerField(default=1)
    discount = models.PositiveSmallIntegerField(default=0)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,
                                 related_name='products',
                                 null=True,blank=True)   
    my_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    ) 
    
    
    class Meta:
        ordering = ['my_order']
    
    @property
    def discounted_price(self):
        if self.discount:
            return self.price * Decimal(f'{(1 - self.discount / 100)}')
        
        return self.price
    
    
    @property
    def get_image_url(self):
        if not self.image:
            return static('app/images/not_found_image.avif')
        return self.image.url
    
    def __str__(self):
        return self.name

# 10_000
 
# 50% 

# discounted_price = price * (1 - discount/ 100)

# Product.objects.all(category = category_id)

# smartfonlar = Category()

# smartfonlar.products.all()


class Order(BaseModel):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f'{self.name} : {self.phone}'
    
    
    
class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        ONE = 1, "⭐ 1"
        TWO = 2, "⭐⭐ 2"
        THREE = 3, "⭐⭐⭐ 3"
        FOUR = 4, "⭐⭐⭐⭐ 4"
        FIVE = 5, "⭐⭐⭐⭐⭐ 5"
    
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments')
    file = models.ImageField(upload_to='comments/%Y/%m/%d/',null=True,blank=True)
    rating = models.PositiveSmallIntegerField(choices=RatingChoices.choices,default = RatingChoices.FIVE)
    is_handle = models.BooleanField(default=False)
    
    

    def __str__(self):
        return f'{self.name} - {self.message}'
    
    
    

# admin@gmail.com
    
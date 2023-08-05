from django.contrib import admin
from app.models import Product,Customer,Cart,OrderPlaced,Trending,DealOfDay

# Register your models here.
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','name','locality','city','zipcode','state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discounted_price',
                  'description','brand','category','product_image']
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity',
                  'ordered_date','status']
    
@admin.register(Trending)
class TrendingModelAdmin(admin.ModelAdmin):
    list_display=['id','trend']

@admin.register(DealOfDay)
class DealOfDayModelAdmin(admin.ModelAdmin):
    list_display=['id','dday']
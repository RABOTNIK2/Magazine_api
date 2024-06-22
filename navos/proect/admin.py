from django.contrib import admin
from .models import *


admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'category', 'rating','price')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('login', 'password')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'delivery_date','owner','products')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('content_review','date')

# Register your models here.

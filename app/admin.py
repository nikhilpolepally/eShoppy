from django.contrib import admin

from app.models import Category, Contact, Order, Product

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Contact)
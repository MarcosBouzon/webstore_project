from django.contrib import admin
from .models import Product, Cart

# Register your models here.
admin.site.register(Product, list_display=["id", "name","price", "image"])
admin.site.register(Cart, list_display=["id", "product"])

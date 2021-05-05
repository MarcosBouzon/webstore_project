from django.contrib import admin
from .models import Product

# Register your models here.
admin.site.register(Product, list_display=["name","price", "image"])

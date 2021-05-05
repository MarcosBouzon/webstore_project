from django.urls import path
from .views import index, product, search, new_product

urlpatterns = [
    path('', index, name="frontend_home"),
    path('product/<int:product_id>/', product, name="frontend_product"),
    path("search/", search, name="frontend_search"),
    path("newproduct/", new_product, name="frontend_new_product"),
]
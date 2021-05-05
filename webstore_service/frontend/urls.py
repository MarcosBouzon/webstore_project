from django.urls import path
from .views import index, product, search

urlpatterns = [
    path('', index, name="frontend_home"),
    path('product/<int:product_id>/', product, name="frontend_product"),
    path("search/", search, name="frontend_search")
]
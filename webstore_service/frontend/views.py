from django.shortcuts import render

import requests


PRODUCTS_URL = "http://localhost:5100/"

def index(request):
    # get products from service
    products = requests.get(f"{PRODUCTS_URL}"+"?query={products { name price image}}")
    print(products)
    if products.ok and products.status_code == 200 and products.json():
        context = {
            "products": products.json().get("products")
        }
        return render(request, "frontend/index.html", context)
    return render(request, "frontend/index.html")


def product(request, product_id):
    return render(request, "frontend/product.html")
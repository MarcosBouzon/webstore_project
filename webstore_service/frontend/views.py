from django.shortcuts import render


def index(request):
    return render(request, "frontend/index.html")

def product(request, product_id):
    return render(request, "frontend/product.html")
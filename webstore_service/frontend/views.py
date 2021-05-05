from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import SearchForm

import requests


PRODUCTS_URL = "http://localhost:5100/"

def index(request):
    form = SearchForm()
    context = {
        "form": form,
    }
    # get products from service
    products = requests.get(f"{PRODUCTS_URL}"+"?query={products { id name price image}}")
    if products.ok and products.status_code == 200 and products.json():
        if products.json().get("products"):
            context["products"] = products.json().get("products")
            return render(request, "frontend/index.html", context)
    # no products in db
    return render(request, "frontend/index.html", context)


def product(request, product_id):
    form = SearchForm()
    # get requested product from service
    products = requests.get(f"{PRODUCTS_URL}"+"?query={product(" + f"productId:{product_id})"+"{ id name description price image}}")
    if products.ok and products.status_code == 200 and products.json():
        context = {
            "form": form,
        }
        if products.json().get("product"):
            context["product"] = products.json().get("product")
            return render(request, "frontend/product.html", context)
        # product doen't exist
        messages.error(request, "The requested product doesn't exist")
    return render(request, "frontend/product.html", context)

def search(request):
    form = SearchForm()
    if request.method == "POST":
        # instance of form with posted data
        form = SearchForm(request.POST)
        if form.is_valid():
            # get requested product from service
            products = requests.get(f"{PRODUCTS_URL}"+"?query={product(" + f"productId:{form['search'].value()})"+"{ id name description price image}}")
            if products.ok and products.status_code == 200 and products.json():
                if products.json().get("product"):
                    context = {
                        "product": products.json().get("product")
                    }
                    return redirect(f"/product/{form['search'].value()}",context=context)
                # product doen't exist
                messages.error(request, "The requested product doesn't exist")
    return redirect(index)
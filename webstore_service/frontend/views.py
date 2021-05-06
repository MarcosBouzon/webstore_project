from django.http.response import HttpResponse
from webstore.settings import STATIC_ROOT
from django.shortcuts import redirect, render
from django.contrib import messages
from urllib.parse import quote
from .forms import SearchForm, NewProduct
from PIL import Image
import requests


PRODUCTS_URL = "http://localhost:5100/"
from .utils import get_cart_items

def index(request):
    cart_items = get_cart_items()
    form = SearchForm()
    context = {
        "form": form,
        "cart_items": cart_items
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
    cart_items = get_cart_items()
    form = SearchForm()
    context = {
        "form": form,
        "cart_items": cart_items
    }
    # get requested product from service
    products = requests.get(f"{PRODUCTS_URL}"+"?query={product(" + f'productId:"{product_id}")'+"{ id name description price image}}")
    if products.ok and products.status_code == 200 and products.json():
        if products.json().get("product"):
            context["product"] = products.json().get("product")
            return render(request, "frontend/product.html", context)
        # product doen't exist
        messages.error(request, "The requested product doesn't exist")
    return render(request, "frontend/product.html", context)

def new_product(request):
    session = requests.session()
    # validating this form is not needed here as its action is not for this route
    form = SearchForm()
    cart_items = get_cart_items()
    # instance of forms
    new_product_form = NewProduct()
    context = {
        "form": form,
        "form_new_product": new_product_form,
        "cart_items": cart_items
    }
    if request.method == "POST":
        # instance of form with data
        new_product_form = NewProduct(request.POST)
        # update dict
        context["form_new_product"] = new_product_form
        if new_product_form.validate():
            # get csrf token from server
            response = session.get(PRODUCTS_URL)
            csrf_token = response.cookies.get("csrftoken")
            mutation = "mutation {" \
                    + f''' createNewProduct(
                            name: "{new_product_form.name.data.lower()}", 
                            description: "{new_product_form.description.data}", 
                            price: {new_product_form.price.data}, 
                            image: "{request.FILES[new_product_form.image.name].name}") ''' \
                        + " { product { name price description image }}}"
            # request product creation
            response = session.post(PRODUCTS_URL, 
                                    headers={"X-CSRFToken": csrf_token}, 
                                    data={"mutation": mutation})
            # created
            if response.ok and response.status_code == 200:
                if response.json() and response.json().get("createNewProduct").get("product"):
                    # get image
                    image = request.FILES[new_product_form.image.name]
                    # attempt to resize image
                    with Image.open(image) as resized_image:
                        resized_image.thumbnail((600, 600))
                        resized_image.save(STATIC_ROOT + f"frontend/images/products/{image.name.lower()}", format="JPEG")
                    messages.success(request, "Your product have been added")
                    return redirect(new_product)
            # failed to create
            else:
                messages.error(request, "Sorry, we couldn't save your product at this time")
                return render(request, "frontend/new_product.html", context)
        # form is not valid
        messages.error(request, "Invalid form")
    return render(request, "frontend/new_product.html", context)

def search(request):
    form = SearchForm()
    if request.method == "POST":
        # instance of form with posted data
        form = SearchForm(request.POST)
        if form.is_valid():
            # get requested product from service
            products = requests.get(f"{PRODUCTS_URL}"+"?query={product(" + f'''productId:"{form['search'].value()}")'''+"{ id name description price image}}")
            if products.ok and products.status_code == 200 and products.json():
                if products.json().get("product"):
                    context = {
                        "product": products.json().get("product")
                    }
                    return redirect(f"/product/{products.json().get('product').get('id')}",context=context)
                # product doen't exist
                messages.error(request, "The requested product doesn't exist")
    return redirect(index)

def cart(request):
    cart_items = get_cart_items()
    context = {
        "cart_items": cart_items
    }
    return HttpResponse(request)








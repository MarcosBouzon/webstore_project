from django.http.response import HttpResponse, JsonResponse
from webstore.settings import STATIC_ROOT
from django.shortcuts import redirect, render
from django.contrib import messages
from django.middleware.csrf import get_token
from urllib.parse import quote
from .forms import SearchForm, NewProduct
from PIL import Image
import requests
from requests.exceptions import ConnectionError, HTTPError


PRODUCTS_URL = "http://products:5100/"
from .utils import get_cart_items, add_cart_item, del_cart_item

def index(request):
    cart_items = get_cart_items()
    form = SearchForm()
    context = {
        "form": form,
        "cart_items": cart_items
    }
    # get products from service
    try:
        if request.GET.get("q"):
            products = requests.get(f"{PRODUCTS_URL}" \
                        + "?query={search (" + f'query:"{request.GET.get("q")}")' \
                        + "{ id name description code price image}}")
        else:
            products = requests.get(f"{PRODUCTS_URL}" \
                + "?query={products { id name code price image}}")
        if products.ok and products.status_code == 200 and products.json():
            # if search requested
            if request.GET.get("q"):
                # search exists
                if products.json().get("search"):
                    context["products"] = products.json().get("search")
                    return render(request, "frontend/index.html", context)
                # search doesn't exist
                else:
                    messages.error(request, "The requested product doesn't exist")
            # no search requested
            elif products.json().get("products"):
                context["products"] = products.json().get("products")
                return render(request, "frontend/index.html", context)
    except (HTTPError, ConnectionError):
        context["products"] = []
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
    try:
        products = requests.get(f"{PRODUCTS_URL}"+"?query={product(" + f'productId:{product_id})'+"{ id name description code price image}}")
        if products.ok and products.status_code == 200 and products.json():
            if products.json().get("product"):
                context["product"] = products.json().get("product")
                return render(request, "frontend/product.html", context)
            # product doen't exist
            messages.error(request, "The requested product doesn't exist")
    except (HTTPError, ConnectionError):
        context["product"] = []
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
            try:
                # get csrf token from server
                response = session.get(PRODUCTS_URL)
                csrf_token = response.cookies.get("csrftoken")
                mutation = "mutation {" \
                        + f''' createNewProduct(
                                name: "{new_product_form.name.data.lower()}", 
                                description: "{new_product_form.description.data}", 
                                code: "{new_product_form.code.data.lower()}", 
                                price: {new_product_form.price.data}, 
                                image: "{request.FILES[new_product_form.image.name].name}") ''' \
                            + " { product { name description code price image }}}"
                # request product creation
                response = session.post(PRODUCTS_URL, 
                                        headers={"X-CSRFToken": csrf_token}, 
                                        data={"mutation": mutation})
                # created
                if response.ok and response.status_code == 200:
                    if response.json() and response.json().get("createNewProduct").get("product"):
                        print(response)
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
            except (HTTPError, ConnectionError):
                messages.error(request, "Sorry, we are having problems at this time adding your product, please try again later")
                return render(request, "frontend/new_product.html", context)
        else:
            # form is not valid
            messages.error(request, "Invalid form")
    return render(request, "frontend/new_product.html", context)

def search(request):
    form = SearchForm()
    if request.method == "POST":
        # instance of form with posted data
        form = SearchForm(request.POST)
        if form.is_valid():
            return redirect(f"/?q={form['search'].value()}")
    return redirect(index)

def cart(request):
    if request.method == "POST":
        action = request.POST.get("action")
        # if add item
        if action == "add":
            # if added
            if add_cart_item(request.POST.get("id")):
                return JsonResponse({"status": "success"}, safe=False)
            # no added
            response = HttpResponse(request)
            response.status_code = 404
            return response
        # if delete
        elif action == "del":
            # if removed
            if del_cart_item(request.POST.get("id")):
                return JsonResponse({"status": "success"}, safe=False)
            # no added
            response = HttpResponse(request)
            response.status_code = 404
            return response
    cart_items = get_cart_items()
    response = JsonResponse(cart_items, safe=False)
    response.headers = {
        "X-CSRFToken": get_token(request)
    }
    return response








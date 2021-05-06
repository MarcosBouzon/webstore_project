import requests
from .views import PRODUCTS_URL


def get_cart_items():
    # get requested product from service
    response = requests.get(f"{PRODUCTS_URL}"+"?query={cartItems {id product { name}}}")
    if response.ok and response.status_code == 200 and response.json().get("cartItems"):
        items = response.json().get("cartItems")
        return items

    return None













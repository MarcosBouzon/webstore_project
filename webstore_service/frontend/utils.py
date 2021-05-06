import requests
from .views import PRODUCTS_URL


def get_cart_items():
    try:
        # get requested product from service
        response = requests.get(f"{PRODUCTS_URL}"+"?query={cartItems {id product {id name price}}}")
        if response.ok and response.status_code == 200 and response.json().get("cartItems"):
            items = response.json().get("cartItems")
            return items
    except requests.exceptions.ConnectionError:
        return None
    return None

def add_cart_item(item_id):
    try:
        # session request
        session = requests.session()
        # get csrf token from server
        response = session.get(PRODUCTS_URL)
        csrf_token = response.cookies.get("csrftoken")
        mutation = 'mutation {addItem(productId: ##) {item {product {id name}}}}'.replace("##", item_id)
        # get requested product from service
        response = session.post(PRODUCTS_URL, headers= {"X-CSRFToken": csrf_token}, data={"mutation": mutation})
        if response.ok and response.status_code == 200 and response.json().get("addItem"):
            return True
    except requests.exceptions.ConnectionError:
        return None
    return False

def del_cart_item(item_id):
    try:
        # session request
        session = requests.session()
        # get csrf token from server
        response = session.get(PRODUCTS_URL)
        csrf_token = response.cookies.get("csrftoken")
        mutation = 'mutation {delItem(cartItemId: ##) {item {product {id name}}}}'.replace("##", item_id)
        # get requested product from service
        response = session.post(PRODUCTS_URL, headers= {"X-CSRFToken": csrf_token}, data={"mutation": mutation})
        print(response.json())
        if response.ok and response.status_code == 200 and response.json().get("delItem"):
            return True
    except requests.exceptions.ConnectionError:
        return None
    return False










from .models import Product, Cart
from django.db.models import Q
from graphene_django import DjangoObjectType

import graphene

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name",  "code","description", "price", "image")


class CartType(DjangoObjectType):
    class Meta:
        model = Cart
        fields = ("id", "product")


class Query(graphene.ObjectType):
    """
    Main Graphql query class
    """
    products = graphene.List(ProductType)
    product = graphene.Field(ProductType, product_id=graphene.Int(default_value=None, required=False))
    search = graphene.List(ProductType, query=graphene.String(default_value=None, required=True))
    cart_items = graphene.List(CartType)

    @staticmethod
    def resolve_products(parent, info):
        queryset = Product.objects.all()
        return queryset
    
    @staticmethod
    def resolve_product(parent, info, product_id):
        if not product_id:
            return None
        # get product with id
        queryset = Product.objects.get(id=product_id)
        return queryset

    @staticmethod
    def resolve_search(parent, info, query):
        print(query)
        if not query:
            return None
        # get product with id or name
        if query:
            queryset = Product.objects.filter(Q(name__contains=query) | Q(code__contains=int(query))).all()
            return queryset

    @staticmethod
    def resolve_cart_items(parent, info):
        queryset = Cart.objects.all()
        return queryset


# mutations handler class
class SaveNewProduct(graphene.Mutation):
    class Arguments:
        # id = graphene.Int()
        name = graphene.String(required=True)
        description = graphene.String()
        code = graphene.String(required=True)
        price = graphene.Float()
        image = graphene.String(required=True)

    product = graphene.Field(ProductType)

    def mutate(parent, info, name, description, code, price, image):
        # new product instance
        new_product = Product(name=name, description=description, code=code, price=price, image=image)
        # save product
        new_product.save()
        # return representation of this mutation
        return SaveNewProduct(product=new_product)


class AddCart(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)
    
    item = graphene.Field(CartType)

    def mutate(parent, info, product_id):
        # get product with id
        product = Product.objects.get(id=product_id)
        if product:
            cart_item = Cart(product=product)
            cart_item.save()
            return AddCart(item=cart_item)


class RemoveCart(graphene.Mutation):
    class Arguments:
        cart_item_id = graphene.Int(required=True)
    
    item = graphene.Field(CartType)

    def mutate(parent, info, cart_item_id):
        queryset = Cart.objects.get(id=cart_item_id)
        queryset.delete()
        return RemoveCart(item=queryset)

# mutation call class
class Mutation(graphene.ObjectType):
    create_new_product = SaveNewProduct.Field()
    add_item = AddCart.Field()
    del_item = RemoveCart.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
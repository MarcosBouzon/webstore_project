import graphene
from .models import Product
from graphene_django import DjangoObjectType

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "description", "price", "image")


class Query(graphene.ObjectType):
    """
    Main Graphql query class
    """
    products = graphene.List(ProductType)
    product = graphene.Field(ProductType, product_id=graphene.Int(default_value=None, required=False))

    @staticmethod
    def resolve_products(parent, info):
        queryset = Product.objects.all()
        return queryset
    
    @staticmethod
    def resolve_product(parent, info, product_id):
        if not product_id:
            return None
        # get product with id or name
        if product_id:
            return Product.objects.get(id=product_id)





schema = graphene.Schema(query=Query)
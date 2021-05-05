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


# mutations handler class
class SaveNewProduct(graphene.Mutation):
    class Arguments:
        # id = graphene.Int()
        name = graphene.String(required=True)
        description = graphene.String()
        price = graphene.Float()
        image = graphene.String(required=True)

    product = graphene.Field(ProductType)

    def mutate(parent, info, name, description, price, image):
        # new product instance
        new_product = Product(name=name, description=description, price=price, image=image)
        # save product
        new_product.save()
        # return representation of this mutation
        return SaveNewProduct(product=new_product)


# mutation call class
class Mutation(graphene.ObjectType):
    create_new_product = SaveNewProduct.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
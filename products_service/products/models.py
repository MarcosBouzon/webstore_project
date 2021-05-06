from django.db import models

class Product(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, auto_created=True)
    name = models.CharField("Name", max_length=50)
    description = models.TextField("Description")
    price = models.FloatField()
    image = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Cart(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, auto_created=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)







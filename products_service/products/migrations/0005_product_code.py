# Generated by Django 3.2.1 on 2021-05-06 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_cart_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='code',
            field=models.CharField(default='', max_length=20, verbose_name='Code'),
        ),
    ]

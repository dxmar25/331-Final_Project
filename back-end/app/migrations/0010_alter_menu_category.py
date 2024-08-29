# Generated by Django 5.0.3 on 2024-04-23 14:23

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    This is a Migration Class written extending/overwriting the Migration class of Django.

    This class is dependent on the operations of "0009_alter_menu_category_alter_menu_description.py"

    This class does the following operations:\n
    - category field in menu has a default choice of Burger (0)\n
    """

    dependencies = [
        ('app', '0009_alter_menu_category_alter_menu_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='category',
            field=models.IntegerField(choices=[(0, 'Burgers'), (1, 'Baskets'), (2, 'Sandwiches'), (3, 'Shakes n Sweets'), (4, 'Beverages'), (5, 'Sides'), (6, 'Sauces')], default=0),
        ),
    ]

# Generated by Django 5.0.3 on 2024-04-18 17:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    This is a Migration Class written extending/overwriting the Migration class of Django.

    This class is dependent on the operations of "0006_alter_inventory_name_alter_menu_description_and_more.py"

    This class does the following operations:\n
    - is_completed in order is removed\n
    - status field in order is added to order with In Progress, Completed, Incomplete, Deleted choices\n
    - season_end field in menu is now a Date Time Field\n 
    - season_start field in menu is no a Date Time Field\n 
    - employee field in order has a Customer foregin Key in user\n 
    - timestamp field in order is now a Date Time Field\n 
    - email field in user is now a Text Field\n 
    - user_type field in user now has choices like Customer, Kitchen, Cashier, Manager, Admin\n 
    """


    dependencies = [
        ('app', '0006_alter_inventory_name_alter_menu_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_completed',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(0, 'In Progress'), (1, 'Completed'), (2, 'Incomplete'), (3, 'Deleted')], default=0),
        ),
        migrations.AlterField(
            model_name='menu',
            name='season_end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='menu',
            name='season_start',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='employee',
            field=models.ForeignKey(default='Customer', on_delete=django.db.models.deletion.DO_NOTHING, to='app.user'),
        ),
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(choices=[(0, 'Customer'), (1, 'Kitchen'), (2, 'Cashier'), (3, 'Manager'), (4, 'Admin')], default=0),
        ),
    ]

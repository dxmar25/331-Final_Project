# Generated by Django 5.0.3 on 2024-04-21 20:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    This is a Migration Class written extending/overwriting the Migration class of Django.

    This class is dependent on the operations of "0007_remove_order_is_completed_order_status_and_more.py"

    This class does the following operations:\n
    - display field in menu is a Boolean Field now with false default value\n
    - employee field in order is a foregin key\n
    """

    dependencies = [
        ('app', '0007_remove_order_is_completed_order_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='display',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='employee',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='app.user'),
        ),
    ]

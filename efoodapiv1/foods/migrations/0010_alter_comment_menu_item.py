# Generated by Django 5.0.6 on 2024-05-08 05:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0009_remove_comment_store_remove_commentstore_menu_item_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='menu_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='foods.menuitem'),
        ),
    ]

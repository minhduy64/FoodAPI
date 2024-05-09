# Generated by Django 5.0.6 on 2024-05-08 05:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0011_rename_comment_reviewmenuitem_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='likemenuitem',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='foods.store'),
        ),
        migrations.AddField(
            model_name='reviewmenuitem',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='foods.store'),
        ),
    ]
# Generated by Django 5.0.1 on 2024-02-27 16:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_color_size_alter_product_managers_product_color_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL),
        ),
    ]
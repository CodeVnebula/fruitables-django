# Generated by Django 5.1.2 on 2024-10-27 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_available',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]

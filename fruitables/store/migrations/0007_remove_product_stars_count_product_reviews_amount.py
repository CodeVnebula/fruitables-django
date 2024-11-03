# Generated by Django 5.1.2 on 2024-11-03 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_product_is_available'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stars_count',
        ),
        migrations.AddField(
            model_name='product',
            name='reviews_amount',
            field=models.IntegerField(default=0),
        ),
    ]
# Generated by Django 5.1.2 on 2024-10-24 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='quantity',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='pack_weight',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]

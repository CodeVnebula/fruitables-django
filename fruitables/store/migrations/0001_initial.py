# Generated by Django 5.1.2 on 2024-10-23 18:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, default='', max_length=255)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='store.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('description', models.TextField()),
                ('detailed_description', models.TextField(blank=True, default='', null=True)),
                ('pack_weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('min_weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('country_of_origin', models.CharField(max_length=255)),
                ('quality', models.CharField(max_length=255)),
                ('health_check', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='product_images/')),
                ('stars', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('stars_count', models.IntegerField(default=0)),
                ('slug', models.SlugField(blank=True, default='', max_length=255, unique=True)),
                ('weight_available', models.FloatField(default=0)),
                ('category', models.ManyToManyField(related_name='products', to='store.category')),
                ('feature', models.ManyToManyField(blank=True, related_name='products', to='store.feature')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewer_name', models.CharField(max_length=100)),
                ('reviewer_email', models.EmailField(max_length=254)),
                ('review', models.TextField()),
                ('stars', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='store.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='review',
            field=models.ManyToManyField(blank=True, related_name='products', to='store.review'),
        ),
    ]

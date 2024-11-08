# Generated by Django 5.1.2 on 2024-11-08 20:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_product_stars_count_product_reviews_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Category name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='store.category', verbose_name='Parent category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=255, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='products', to='store.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='country_of_origin',
            field=models.CharField(max_length=255, verbose_name='Country of origin'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='detailed_description',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Detailed description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='health_check',
            field=models.CharField(max_length=255, verbose_name='Health check'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_available',
            field=models.BooleanField(blank=True, default=True, verbose_name='Is available'),
        ),
        migrations.AlterField(
            model_name='product',
            name='min_weight',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Min weight'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Product name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pack_weight',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Pack weight'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='quality',
            field=models.CharField(max_length=255, verbose_name='Quality'),
        ),
        migrations.AlterField(
            model_name='product',
            name='review',
            field=models.ManyToManyField(blank=True, related_name='products', to='store.review', verbose_name='Review'),
        ),
        migrations.AlterField(
            model_name='product',
            name='reviews_amount',
            field=models.IntegerField(default=0, verbose_name='Reviews amount'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=255, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='product',
            name='stars',
            field=models.IntegerField(default=0, verbose_name='Stars'),
        ),
        migrations.AlterField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='products', to='store.tag', verbose_name='Tag'),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_available',
            field=models.FloatField(default=0, verbose_name='Weight available'),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='review',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='store.product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.TextField(verbose_name='Review'),
        ),
        migrations.AlterField(
            model_name='review',
            name='reviewer_email',
            field=models.EmailField(max_length=254, verbose_name='Reviewer email'),
        ),
        migrations.AlterField(
            model_name='review',
            name='reviewer_name',
            field=models.CharField(max_length=100, verbose_name='Reviewer name'),
        ),
        migrations.AlterField(
            model_name='review',
            name='stars',
            field=models.IntegerField(default=0, verbose_name='Stars'),
        ),
    ]
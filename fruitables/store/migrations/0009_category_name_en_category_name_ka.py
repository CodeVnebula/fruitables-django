# Generated by Django 5.1.2 on 2024-11-08 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_category_name_alter_category_parent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Category name'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ka',
            field=models.CharField(max_length=255, null=True, verbose_name='Category name'),
        ),
    ]

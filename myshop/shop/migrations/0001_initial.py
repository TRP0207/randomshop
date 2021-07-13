# Generated by Django 3.0.5 on 2020-04-28 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(db_index=True, max_length=200)),
                ('category_slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['category_name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(db_index=True, max_length=200)),
                ('product_slug', models.CharField(db_index=True, max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='product/%Y/%m/%d')),
                ('description', models.TextField(blank=True)),
                ('available', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='shop.Category')),
            ],
            options={
                'ordering': ('product_name',),
                'index_together': {('id', 'product_slug')},
            },
        ),
    ]

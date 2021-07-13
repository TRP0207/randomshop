from django.db import models
from django.urls import reverse
# Create your models here.


class Category(models.Model):

    category_name = models.CharField(max_length=200, db_index=True,)
    category_slug = models.SlugField(max_length=200, unique=True)


    class Meta:
        ordering = ['category_name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.category_slug])

    def __str__(self):
        return self.category_name


class Product(models.Model):

    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200, db_index=True)
    product_slug = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('product_name',)
        index_together = (('id', 'product_slug'),)

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.product_slug])

    def __str__(self):
        return self.product_name























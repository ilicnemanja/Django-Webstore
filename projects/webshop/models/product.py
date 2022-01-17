from django.db import models
from django.urls import reverse

from . import category, user

class Product(models.Model):
    category = models.ForeignKey(category.Category, related_name='products', on_delete=models.CASCADE)
    user = models.ForeignKey(user.User, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to="products", blank=True, default="nophoto.jpg")
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("webshop:product_detail", args=[self.id, self.slug])
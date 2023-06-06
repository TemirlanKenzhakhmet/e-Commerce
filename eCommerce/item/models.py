from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.urls import reverse
from django_countries.fields import CountryField
from django.db.models import Q

from .utils import slugify_instance

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name',]
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class ItemQuerySet(models.QuerySet):
    def search(self, query = None):
        if not query:
            return self.none()
        lookups = Q(name__icontains=query) | Q(description__icontains=query)
        return self.filter(lookups)

class ItemManager(models.Manager):
    def get_queryset(self):
        return ItemQuerySet(self.model, using=self._db)
    
    def search(self, query = None):
        return self.get_queryset().search(query = query)

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    slug = models.SlugField(unique = True, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    likes = models.PositiveIntegerField(default=0)

    objects = ItemManager()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('item:detail', kwargs={'slug': self.slug})
    
    def get_add_to_cart_url(self):
        return reverse('item:add-to-cart', kwargs={'slug': self.slug})
    
    def get_remove_from_cart_url(self):
        return reverse('item:remove-from-cart', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

def item_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance(instance)

pre_save.connect(item_pre_save, sender=Item)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"
    
    def get_total_item_price(self):
        return "%.2f" % (self.quantity * self.item.price)
    
    def get_total_discount_item_price(self):
        return "%.2f" % (self.quantity * self.item.discount_price)

    def get_amount_saved(self):
        return "%.2f" % ((self.quantity * self.item.price) - (self.quantity * self.item.discount_price))
    
    def get_final_price(self):
        if self.item.discount_price:
            return self.quantity * self.item.discount_price
        return self.quantity * self.item.price


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return "%.2f" % total if total else 0


class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

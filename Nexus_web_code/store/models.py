

# Create your models here.
from django.conf import settings
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=120)
    brand = models.CharField(max_length=60)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.brand} {self.name}"

class SKU(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="skus")
    color = models.CharField(max_length=40)
    storage = models.CharField(max_length=40)
    sku_code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.product} — {self.storage} — {self.color}"

class Price(models.Model):
    sku = models.OneToOneField(SKU, on_delete=models.CASCADE, related_name="price")
    list_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default="USD")

class Inventory(models.Model):
    sku = models.OneToOneField(SKU, on_delete=models.CASCADE, related_name="inventory")
    qty_on_hand = models.PositiveIntegerField(default=0)

class Order(models.Model):
    STATUS_CHOICES = [("NEW","NEW"),("PAID","PAID"),("CANCELLED","CANCELLED")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="NEW")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    sku = models.ForeignKey(SKU, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

class CartItem(models.Model):
    session_key = models.CharField(max_length=40, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("session_key", "sku")

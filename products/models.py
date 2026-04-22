# models.py
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):

    CATEGORY_CHOICES = (
        ('web', 'Web Templates'),
        ('mobile', 'Mobile Apps'),
        ('plugin', 'Plugins & Extensions'),
        ('graphics', 'Graphics & Icons'),
        ('course', 'Courses & Tutorials'),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=255)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    rating = models.FloatField(default=0) 
    is_active = models.BooleanField(default=True) 

    project_file = models.FileField(
        upload_to='product_files/',
        blank=True,
        null=True
    )
    def __str__(self):
        return self.title
    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    approved = models.BooleanField(default=False)
    payment_screenshot = models.ImageField(
    upload_to="payments/",
    null=True,
    blank=True
)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
     product_title = self.product.title if self.product else "No Product"
     return f"{self.user.username} - {product_title}"



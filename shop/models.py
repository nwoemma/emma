from django.db import models

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Categories,related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=11,decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    ordered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Order of {self.quantity} x {self.product.name}'

class Booking(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    persons = models.PositiveIntegerField()
    booking_date = models.DateField()

    def __str__(self):
        return f"Booking for {self.name} on {self.booking_date}"

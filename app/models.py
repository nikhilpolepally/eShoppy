from django.db import models

# Create your models here.


class Category(models.Model):
    category_id = models.AutoField
    category = models.CharField(max_length=100, default="")
    slug = models.SlugField(max_length=100, default="")

    def __str__(self):
        return self.category


class Product(models.Model):
    product_id = models.AutoField
    brand = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
    )
    deals = models.CharField(max_length=100, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    contact_id = models.AutoField
    name= models.CharField(max_length=100, default="")
    email= models.CharField(max_length=100)
    subject= models.CharField(max_length=1000)
    message= models.CharField(max_length=5000)
    def __str__(self):
        return self.email


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_items = models.CharField(max_length=5000)
    amount = models.CharField(max_length=90)
    name = models.CharField(max_length=90)
    delivery_email = models.CharField(max_length=90)
    user_email = models.CharField(
        max_length=90, blank=True, null=True, default=False)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=1000, blank=True, null=True)
    signature_id = models.CharField(max_length=1000, blank=True, null=True)
    signature_id = models.CharField(max_length=1000, blank=True, null=True)
    oid = models.CharField(max_length=150, blank=True)
    amount_paid = models.CharField(max_length=500, blank=True, null=True)
    payment_status = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=100, default="")
    delievery_description = models.CharField(default=False, max_length=5000)
    isdelivered = models.BooleanField(default=False)

    def __str__(self):
        return self.name

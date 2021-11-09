from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=200, null=True)
    email=models.CharField(max_length=200, null=True)
#
#     def __str__(self):
#         return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)
    # slug=models.SlugField()
    #image


    def __str__(self):
        return self.name
    #
    # def get_absolute_url(self):
    #     return reverse("store:product", kwargs={'slug':self.slug})

    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)


    def __str__(self):
        return str(self.id)

    @property
    def all_cart_value(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def all_cart_quantity(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total=self.product.price*self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    postcode = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    date_added = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.address

# class Item
# Create your models here.

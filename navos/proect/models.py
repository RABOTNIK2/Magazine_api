from django.db import models
from django.core.validators import MaxValueValidator
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)], null=True)
    image = models.TextField()
    price = models.PositiveIntegerField(null=True)
    
    def __str__(self):
        return f'{self.name}, {self.image}, {self.description}, {self.price}'
    

class User(models.Model):
    login = models.CharField(max_length=70)
    password = models.CharField(max_length=32)
    image = models.TextField(blank=True,default='https://avatars.mds.yandex.net/i?id=4e2584ffe6be91882307ebaff5ac63a1f173f9fb-11526326-images-thumbs&n=13')
    cart = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return f'{self.login}, {self.image}'

class Order(models.Model):
    number = models.PositiveIntegerField()
    delivery_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='owner')
    products = models.ForeignKey(User, on_delete=models.DO_NOTHING , related_name='products')

class Review(models.Model):
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    content_review = models.TextField()
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)], null=True)

    def __str__(self):
        return self.content_review


# Create your models here.

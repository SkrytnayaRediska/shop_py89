from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Discount(models.Model):
    percent = models.IntegerField()
    name = models.CharField(max_length=20)
    date_start = models.DateField()
    date_end = models.DateField()

    def __str__(self):
        return self.name


class Promocode(models.Model):
    name = models.CharField(max_length=10)
    percent = models.IntegerField()
    date_start = models.DateField()
    date_end = models.DateField()
    is_cumulative = models.BooleanField()

    def __str__(self):
        return self.name


class Seller(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.country}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    articul = models.CharField(max_length=20)
    description = models.TextField()
    count_on_stock = models.IntegerField()
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

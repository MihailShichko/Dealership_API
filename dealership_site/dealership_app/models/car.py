from django.contrib.auth.models import User
from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=255)
    manufacture_date = models.DateField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    horsepower = models.IntegerField()
    cat = models.ForeignKey("Manufacturer", on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
from django.db import models

class Rate(models.Model):
    source_currency = models.CharField(max_length=3)
    destination_currency = models.CharField(max_length=3)
    date = models.DateField()
    rate = models.DecimalField(max_digits=15, decimal_places=5, default=0)
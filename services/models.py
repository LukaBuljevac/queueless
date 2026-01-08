from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=120)
    duration_min = models.PositiveIntegerField(default=30)
    price_eur = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self) -> str:
        return self.name

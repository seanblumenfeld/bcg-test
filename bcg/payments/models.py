from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Ledger(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    movement_type = models.CharField(
        choices=[('charge', 'charge')],
        max_length=6,
        blank=False,
        null=False

    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    token = models.TextField()

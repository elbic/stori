import uuid

from django.db import models


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_id = models.IntegerField()
    date = models.DateField()
    kind = models.CharField(max_length=6)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("transaction_id", "date")

    def __str__(self):
        return f"{self.kind}, {self.amount}"

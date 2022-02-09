from django.db import models


class Transaction(models.Model):
    tx_id = models.CharField("Transaction ID", primary_key=True, max_length=100)
    description = models.TextField('Description')

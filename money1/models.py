from django.db import models


class Expense(models.Model):
    name = models.CharField(max_length=30)
    value = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name

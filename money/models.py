from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=30, help_text='Введите название категории.')

    def __str__(self):
        return self.name


class Expense(models.Model):
    value = models.PositiveIntegerField(help_text='Введите значение.')
    category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL,
                                 help_text='Выберите категорию из предложенных.', related_name='category')
    description = models.CharField(max_length=100, blank=True, help_text='Введите описание расходов.')
    date = models.DateField(null=False, auto_now_add=False)
    created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Расход {self.value} рублей.'

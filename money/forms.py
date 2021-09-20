from django.forms import ModelForm
from .models import Expense, Category, Plan


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['value', 'category', 'description', 'date']


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = ['title', 'value']

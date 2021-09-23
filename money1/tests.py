from django.test import TestCase

import pytest
from money1.models import Expense


@pytest.mark.expense
def test_it_creates_expense():
    Expense.objects.create(name='pizza',
                           value='1')
    assert Expense.objects.count() == 1


# class ExpenseTestCase(TestCase):
#     def setUp(self):
#         Expense.objects.create(name="lion", value='1')
#         Expense.objects.create(name="cat", value="2")

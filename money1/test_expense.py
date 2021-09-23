import pytest
from money1.models import Expense


@pytest.mark.expense
def test_it_creates_expense():
    Expense.objects.create(name='pizza',
                           value='1')
    assert Expense.objects.count() == 1

from django.contrib import admin
from money.models import Category, Expense

admin.site.register(Category)


class ExpenseAdmin(admin.ModelAdmin):
    readonly_fields = ('created', )


admin.site.register(Expense, ExpenseAdmin)

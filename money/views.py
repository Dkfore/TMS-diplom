from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import ExpenseForm, CategoryForm, PlanForm
from django.contrib.auth.decorators import login_required
import matplotlib
from matplotlib import pyplot as plt
from io import BytesIO
import base64
from money.serializers import ExpenseSerializer, UserSerializer, CategorySerializer
from money.models import Expense, Category, Plan
from rest_framework import viewsets
from rest_framework import permissions
from django.shortcuts import render
matplotlib.use('Agg')

FILTERS_ALL_CATEGORIES_ID = -1


def home(request):
    return render(request, 'money/home.html')


'''user'''


def signup_user(request):
    if request.method == "GET":
        return render(request, 'money/user/signup_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('all_expenses')
            except IntegrityError:
                return render(request, 'money/user/signup_user.html', {'form': UserCreationForm(),
                                                                       'error': 'Такой пользователь уже существует.'})
        else:
            return render(request, 'money/user/signup_user.html', {'form': UserCreationForm(),
                                                                   'error': 'Пароли не совпадают.'})


def login_user(request):
    if request.method == "GET":
        return render(request, 'money/user/login_user.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'money/user/login_user.html', {'form': AuthenticationForm(),
                                                                  'error': 'Проверьте правильность логина и пароля.'})
        else:
            login(request, user)
            return redirect('all_expenses')


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


'''Expense'''


@login_required
def all_expenses(request):
    categories = Category.objects.all()
    content = {
        'categories': categories,
        'filters': {
            'category_id': FILTERS_ALL_CATEGORIES_ID,
        },
    }
    category_id = int(request.GET.get('category_id', FILTERS_ALL_CATEGORIES_ID))
    content['filters']['category_id'] = category_id
    total_count = 0
    if category_id != FILTERS_ALL_CATEGORIES_ID:
        content['expenses'] = Expense.objects.filter(category__id=category_id, user=request.user)
        for expense in content['expenses']:
            total_count += expense.value

    else:
        content['expenses'] = Expense.objects.filter(user=request.user)
        for expense in content['expenses']:
            total_count += expense.value

    content['total_count'] = total_count

    '''graphs'''

    list_category = []
    for i in list(Category.objects.all()):
        list_category.append(i.name)
    values_list = []
    for category in list_category:
        values_list1 = Expense.objects.filter(category__name=category, user=request.user)
        cat_value = 0
        for cat in values_list1:
            cat_value += cat.value
        values_list.append(cat_value)
    fig1, ax1 = plt.subplots()

    def make_autopct(values_list):
        def my_autopct(pct):
            total = sum(values_list)
            val = int(round(pct * total / 100.0))
            return '{p:.2f}%  ({v:d} руб)'.format(p=pct, v=val)

        return my_autopct

    ax1.pie(values_list, labels=list_category, autopct=make_autopct(values_list),
            shadow=True, startangle=90)
    ax1.axis('equal')
    buf = BytesIO()
    plt.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    content['data'] = data

    return render(request, 'money/expenses/all_expenses.html', content)


def create_expense(request):
    if request.method == "GET":
        return render(request, 'money/expenses/create_expense.html', {'form': ExpenseForm()})
    else:
        try:
            form = ExpenseForm(request.POST)
            new_expense = form.save(commit=False)
            new_expense.user = request.user
            new_expense.save()
            return redirect('all_expenses')
        except ValueError:
            return render(request, 'money/expenses/create_expense.html', {'form': ExpenseForm(),
                                                                          'error': 'Неверные данные'})


def view_expense(request, expense_pk):
    expense = get_object_or_404(Expense, pk=expense_pk, user=request.user)
    if request.method == 'GET':
        form = ExpenseForm(instance=expense)
        return render(request, 'money/expenses/view_expense.html', {'expense': expense, 'form': form})
    else:
        try:
            form = ExpenseForm(request.POST, instance=expense)
            form.save()
            return redirect('all_expenses')
        except ValueError:
            return render(request, 'money/expenses/create_expense.html',
                          {'expense': expense, 'form': ExpenseForm(), 'error': 'Неверные данные'})


def delete_expense(request, expense_pk):
    expense = get_object_or_404(Expense, pk=expense_pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('all_expenses')


'''Category'''


def all_category(request):
    categories = Category.objects.all()
    content = {
        'categories': categories
    }
    return render(request, 'money/category/all_category.html', content)


def create_category(request):
    if request.method == "GET":
        return render(request, 'money/category/create_category.html', {'form': CategoryForm()})
    else:
        try:
            form = CategoryForm(request.POST)
            new_category = form.save(commit=False)
            new_category.user = request.user
            new_category.save()
            return redirect('all_category')
        except ValueError:
            return render(request, 'money/category/create_category.html', {'form': CategoryForm(),
                                                                           'error': 'Неверные данные'})


def view_category(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    if request.method == 'GET':
        form = CategoryForm(instance=category)
        return render(request, 'money/category/view_category.html', {'category': category, 'form': form})
    else:
        try:
            form = CategoryForm(request.POST, instance=category)
            form.save()
            return redirect('all_category')
        except ValueError:
            return render(request, 'money/category/create_category.html',
                          {'category': 'category', 'form': CategoryForm(), 'error': 'Неверные данные'})


def delete_category(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    if request.method == 'POST':
        category.delete()
        return redirect('all_category')


''' Планирование расходов '''


def plan(request):
    plan = Plan.objects.all()
    total_count = 0
    for i in plan:
        total_count += i.value

    content = {
        'plan': plan,
        'total_count': total_count,
    }
    return render(request, 'money/plan/plan.html', content)


def create_plan(request):
    if request.method == "GET":
        return render(request, 'money/plan/create_plan.html', {'form': PlanForm()})
    else:
        try:
            form = PlanForm(request.POST)
            new_category = form.save(commit=False)
            new_category.user = request.user
            new_category.save()
            return redirect('plan')
        except ValueError:
            return render(request, 'money/plan/create_plan.html', {'form': PlanForm(),
                                                                   'error': 'Неверные данные'})


def view_plan(request, plan_pk):
    plan = get_object_or_404(Plan, pk=plan_pk)
    if request.method == 'GET':
        form = PlanForm(instance=plan)
        return render(request, 'money/plan/view_plan.html', {'plan': plan, 'form': form})
    else:
        try:
            form = PlanForm(request.POST, instance=plan)
            form.save()
            return redirect('plan')
        except ValueError:
            return render(request, 'money/plan/create_plan.html',
                          {'plan': 'plan', 'form': CategoryForm(), 'error': 'Неверные данные'})


def delete_plan(request, plan_pk):
    plan = get_object_or_404(Plan, pk=plan_pk)
    if request.method == 'POST':
        plan.delete()
        return redirect('plan')


def delete_all(request):
    plan = Plan.objects.all().delete()

    return render(request, 'money/plan/delete_all.html')


''' API '''


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

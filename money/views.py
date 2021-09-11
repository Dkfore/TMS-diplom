from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExpenseForm, CategoryForm
from .models import Expense, Category


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

    if category_id != FILTERS_ALL_CATEGORIES_ID:
        content['expenses'] = Expense.objects.filter(category__id=category_id)
    else:
        content['expenses'] = Expense.objects.filter(user=request.user)

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
                          {'expense': 'expense', 'form': ExpenseForm(), 'error': 'Неверные данные'})


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

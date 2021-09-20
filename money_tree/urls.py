"""money_tree URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from money import views



from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('all_expenses/', views.all_expenses, name='all_expenses'),
    path('expense/', views.create_expense, name='create_expense'),
    path('expense/<int:expense_pk>', views.view_expense, name='view_expense'),
    path('expense/<int:expense_pk>/delete', views.delete_expense, name='delete_expense'),


    # Auth
    path('signup/', views.signup_user, name='signup_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('login/', views.login_user, name='login_user'),


    # Category
    path('category/', views.all_category, name='all_category'),
    path('category/create', views.create_category, name='create_category'),
    path('category/<int:category_pk>', views.view_category, name='view_category'),
    path('category/<int:category_pk>/delete', views.delete_category, name='delete_category'),

    #plan
    path('plan/', views.plan, name='plan'),
    path('plan/create', views.create_plan, name='create_plan'),
    path('plan/<int:plan_pk>', views.view_plan, name='view_plan'),
    path('plan/<int:plan_pk>/delete', views.delete_plan, name='delete_plan'),
    path('plan/delete_all', views.delete_all, name='delete_all'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""inpatientsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from inpatientsystemApp import views

urlpatterns = [
    path('', views.homepage),
    path('admin/', admin.site.urls, name='admin'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_workspace/', views.admin_workspace, name='admin_workspace'),
    path('doctor_login/', views.singup_doctor_form, name='doctor_login'),
    path('add_user/', views.add_user, name='add_user'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
]

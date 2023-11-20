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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('admin/', admin.site.urls, name='admin'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_workspace/', views.admin_workspace, name='admin_workspace'),
    path('add_user/', views.add_user, name='add_user'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('doctor_login/', views.doctor_login, name='doctor_login'),
    path('doctor_workspace/', views.doctor_workspace, name='doctor_workspace'),
    path('doctor_sign_up/', views.doctor_sign_up, name='doctor_sign_up'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('doctor_logout/', views.doctor_logout, name='doctor_logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from inpatientsystem import forms
from django.contrib.auth import login, authenticate # import des fonctions login et authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms as dj_form
from django.contrib import messages
from django.shortcuts import render, redirect

def homepage(request,):
    return render(request, "homepage.html", {"name": "Mamitiana"})
def add(request, class_forms, template, redirect_page):
    if not request.user.is_staff:
        messages.error(request, "Access denied")
        return redirect(redirect_page)

    form_class = getattr(forms, class_forms, None)

    if not form_class:
        messages.error(request, "Invalid form class")
        return redirect(redirect_page)

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            user = form.save()
            #messages.success(request, f'{user.username} is added successfully!')
            return redirect(redirect_page)
    else:
        form = form_class()

    return render(request, template, {'form': form})

def add_user(request):
    return add(request, 'SuperuserCreationForm', 'add_user.html', 'admin_workspace')

def add_doctor(request):
    return add(request, 'DoctorForm', 'add_doctor.html', 'admin_workspace')

def admin_login(request):
    form = forms.admin_login_Form()
    message = ''
    if request.method == 'POST':
        form = forms.admin_login_Form(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Hello, {user.username}! You are connected successfully.'
                return redirect('admin_workspace')
            else:
                message = 'Invalid identifier or password'
    return render(
        request, 'admin_login.html', context={'form': form, 'message': message})

def admin_workspace(request):
    return render(request, "admin_workspace.html", {"name" : "Mamitiana"})

@login_required
def admin_django(request):
    if request.user.is_staff:
        return render(request, 'admin_django.html')
    else:
        # Gérer le cas où l'utilisateur n'est pas membre du personnel
        #return render(request, 'non_staff_template.html')
        return redirect('homepage.html')# template à crer et à modifier
@login_required
def add_superuser(request):
    if not request.user.is_staff:
        messages.error(request, "Access dined")
        return redirect('homepage')

    if request.method == 'POST':
        form = forms.SuperuserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} is added successfully!')
            return redirect('admin_workspace')
    else:
        form = forms.SuperuserCreationForm()

    return render(request, 'add_user.html', {'form': form})
def singup_doctor_form(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Hello, {user.username}! You are connected successfully.'
            else:
                message = 'Invalid identifier or password'
    return render(
        request, 'doctor_login.html', context={'form': form, 'message': message})

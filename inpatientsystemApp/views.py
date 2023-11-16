from inpatientsystem import forms
from django.contrib.auth import login, authenticate # import des fonctions login et authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
def homepage(request,):
    return render(request, "homepage.html", {"name" : "Mamitiana"})

def click_admin(request,):
    return render(request, "admin_workspace.html", {"name" : "Mamitiana"})

def click_doctor(request,):
    return render(request, "doctorclick.html", {"name" : "Mamitiana"})

def singup_admin_form(request):
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
                return redirect('admin_workspace')
            else:
                message = 'Invalid identifier or password'
    return render(
        request, 'admin_login.html', context={'form': form, 'message': message})

def admin_workspace(request):
    return render(request, "admin_workspace.html", {"name" : "Mamitiana"})

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
@login_required
def add_doctor(request):
    if not request.user.is_staff:
        messages.error(request, "Access dined")
        return redirect('homepage')

    if request.method == 'POST':
        form = forms.DoctorUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} is added successfully!')
            return redirect('admin_workspace')
    else:
        form = forms.SingupForm()

    return render(request, 'add_user.html', {'form': form})

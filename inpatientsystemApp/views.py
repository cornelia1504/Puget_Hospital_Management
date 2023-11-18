from inpatientsystem import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.views import LogoutView

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

@login_required
def add_user(request):
    return add(request, 'UserCreationForm', 'add_user.html', 'admin_workspace')

@login_required
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

@login_required
def admin_workspace(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied")
        return redirect(admin_login)
    return render(request, "admin_workspace.html", {"name" : "Mamitiana"})

@login_required
def admin_django(request):
    if request.user.is_staff:
        return render(request, 'admin_django.html')
    else:
        # Gérer le cas où l'utilisateur n'est pas membre du personnel
        #return render(request, 'non_staff_template.html')
        return redirect('homepage.html')# template à crer et à modifier

def doctor_login(request):
    form = forms.doctor_login_Form()
    message = ''
    if request.method == 'POST':
        form = forms.doctor_login_Form(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                #message = f'Hello, {user.username}! You are connected successfully.'
                return redirect('doctor_workspace')
            else:
                message = 'Invalid identifier or password'
    return render(
        request, 'doctor_login.html', context={'form': form, 'message': message})

def doctor_workspace(request):
    current_date = datetime.now()
    return render(request, "doctor_workspace.html", {'current_date': current_date})

def doctor_sign_up(request):
    form = forms.Doctor_sign_up_Form()
    message = ''
    if request.method == 'POST':
        form = forms.Doctor_sign_up_Form(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                user = form.save()
                login(request, user)
                return redirect('doctor_login')
            else:
                message = 'Invalid identifier or password'
    return render(
        request, 'doctor_sign_up.html', context={'form': form, 'message': message})

def admin_logout(request):
    return LogoutView.as_view()(request)
def doctor_logout(request):
    return redirect(homepage)

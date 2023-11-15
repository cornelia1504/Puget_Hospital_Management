
from django.shortcuts import render
from inpatientsystem import forms
from django.contrib.auth import login, authenticate # import des fonctions login et authenticate

def homepage(request,):
    return render(request, "homepage.html", {"name" : "Mamitiana"})

def click_admin(request,):
    return render(request, "adminclick.html", {"name" : "Mamitiana"})

def click_doctor(request,):
    return render(request, "doctorclick.html", {"name" : "Mamitiana"})

def singup_form(request):
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
                message = f'Bonjour, {user.username}! Vous êtes connecté.'
            else:
                message = 'Identifiants invalides.'
    return render(
        request, 'login.html', context={'form': form, 'message': message})



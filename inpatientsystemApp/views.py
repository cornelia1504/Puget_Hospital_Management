
from django.shortcuts import render



def homepage(request,):
    return render(request, "homepage.html", {"name" : "Mamitiana"})

def click_admin(request,):
    return render(request, "adminclick.html", {"name" : "Mamitiana"})

def click_doctor(request,):
    return render(request, "doctorclick.html", {"name" : "Mamitiana"})




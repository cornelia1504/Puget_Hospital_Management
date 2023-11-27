from django.http import HttpResponseRedirect

from inpatientsystem import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from .models import Bed, OperatingRoomSchedule, OperatingRoom, Doctor
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from inpatientsystem.forms import DoctorSignupForm
from inpatientsystem.forms import DoctorUserForm, DoctorForm, OperationPerformingForm, OperatingRoomScheduleForm, OperationForm
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_protect
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

def my_operation(request):

    # 假设你已经在视图中获取了当前登录的医生用户
    current_doctor = request.user.doctor

    # 获取当前登录医生的所有 OperationPerforming 行
    doctor_operations = OperationPerformingForm.objects.filter(id_doctor=current_doctor)

    context = {
        'doctor_operations': doctor_operations,
    }
def add_patient(request):
    return add(request,'PatientForm', 'add_patient.html','doctor_workspace')


def add_operation(request):
    if request.method == 'POST':
        # 根据提交的表单类型，创建相应的表单实例
        form_type = request.POST.get('form_type')  # 假设有一个隐藏的表单字段指示表单类型
        if form_type == 'operating_room_schedule':
            form = OperatingRoomScheduleForm(request.POST)
        elif form_type == 'operation_performing':
            form = OperationPerformingForm(request.POST)
        elif form_type == 'operation':
            form = OperationForm(request.POST)
        else:
            # 处理未知的表单类型
            return render(request, 'error_page.html', {'error_message': 'Unknown form type'})

        # 检查表单是否有效
        if form.is_valid():
            # 保存表单数据
            form.save()

            # 重定向到 doctor_workspace
            return redirect('doctor_workspace')
        else:
            # 处理表单验证失败的情况
            return render(request, 'error_page.html', {'error_message': 'Form validation failed'})
    else:
        # 如果是 GET 请求，创建一个空的表单实例
        operating_room_schedule_form = OperatingRoomScheduleForm()
        operation_performing_form = OperationPerformingForm()
        operation_form = OperationForm()

        return render(request, 'add_operation.html', {
            'operating_room_schedule_form': operating_room_schedule_form,
            'operation_performing_form': operation_performing_form,
            'operation_form': operation_form,
        })


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

# def doctor_workspace(request):
#     current_date = datetime.now()
#     return render(request, "doctor_workspace.html", {'current_date': current_date})


def doctor_workspace(request):
    # 计算 bed_occupied 和 operating_room_occupied 的信息
    total_beds = Bed.objects.count()
    occupied_beds = Bed.objects.exclude(id_patient=None).count()
    bed_occupied = (occupied_beds / total_beds) * 100 if total_beds > 0 else 0

    total_operating_rooms = OperatingRoom.objects.count()
    occupied_operating_rooms = OperatingRoomSchedule.objects.count()
    operating_room_occupied = (occupied_operating_rooms / total_operating_rooms) * 100 if total_operating_rooms > 0 else 0

    context = {
        'doctor': request.user.doctor,
        'bed_occupied': round(bed_occupied, 1),
        'operating_room_occupied': round(operating_room_occupied, 1),
    }

    return render(request, 'doctor_workspace.html', context)


# def doctor_sign_up(request):
#     form = forms.DoctorUserForm()
#     message = ''
#     if request.method == 'POST':
#         form = forms.DoctorUserForm(request.POST)
#         if form.is_valid():
#             user = authenticate(
#                 username=form.cleaned_data['username'],
#                 password=form.cleaned_data['password'],
#             )
#             if user is not None:
#                 user = form.save()
#                 login(request, user)
#                 return redirect('doctor_login')
#             else:
#                 message = 'Invalid identifier or password'
#     return render(
#         request, 'doctor_sign_up.html', context={'form': form, 'message': message})

# def doctor_signup_view(request):
#     form = DoctorSignupForm()
#     if request.method == 'POST':
#         form = DoctorSignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.set_password(form.cleaned_data['password1'])
#             user.save()
#             my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
#             my_doctor_group[0].user_set.add(user)
#             return HttpResponseRedirect('doctor_login')
#
#     return render(request, 'doctor_sign_up.html', context={'form': form})


def doctor_signup_view(request):
    user_form = DoctorUserForm()
    doctor_form = DoctorForm()
    mydict = {'userForm': user_form, 'doctorForm': doctor_form}
    if request.method == 'POST':
        user_form = forms.DoctorUserForm(request.POST)
        doctor_form = forms.DoctorForm(request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor = doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctor_login')
    return render(request, 'doctor_sign_up.html', context=mydict)

def admin_logout(request):
    return LogoutView.as_view()(request)
def doctor_logout(request):
    return redirect(homepage)
@login_required
def add_operatingroomschedule(request):
    return add(request, 'OperatingRoomScheduleForm', 'add_operatingroomschedule.html', 'admin_workspace')


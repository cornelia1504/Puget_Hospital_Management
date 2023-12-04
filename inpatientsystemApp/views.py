from turtle import pd

from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from .models import Patient
from .serializers import PatientSerializer
from inpatientsystem import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from datetime import datetime
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from .models import Bed, OperatingRoomSchedule, OperatingRoom, Doctor, Operation, Patient
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from inpatientsystem.forms import DoctorForm, OperatingRoomScheduleForm, OperationForm, PatientForm, BedForm
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse


# ---------------------------------------------------------------------------------
# ------------------------ INFORMATION PAGES --------------------------------------
# ---------------------------------------------------------------------------------
def homepage(request, ):
    return render(request, "homepage.html", {"name": "Mamitiana"})





def login_page(request, ):
    return render(request, "login.html")


def info_page(request, ):
    return render(request, "info_page.html")


def contact(request, ):
    return render(request, "contact_page.html")


# ---------------------------------------------------------------------------------
# ---------------------------------------ADD---------------------------------------
# ---------------------------------------------------------------------------------
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
            messages.success(request, f'Add successfully!')
            return redirect(redirect_page)
    else:
        form = form_class()
        messages.success(request, f'Password look same as username')

    return render(request, template, {'form': form})


# ---------------------------------------------------------------------------------
# ------------------------ ADMIN RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
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
    return render(request, "admin_workspace.html")


# def admin_workspace(request):
#     if not request.user.is_staff:
#         messages.error(request, "Access denied")
#         return redirect(admin_login)
#     return render(request, "admin_workspace.html", {"name" : "Mamitiana"})


@login_required
def add_user(request):
    return add(request, 'UserCreationForm', 'add_user.html', 'add_user')


@login_required
def add_doctor(request):
    return add(request, 'DoctorForm', 'add_doctor.html', 'add_doctor')


@login_required
def admin_django(request):
    if request.user.is_staff:
        return render(request, 'admin_django.html')
    else:
        # Gérer le cas où l'utilisateur n'est pas membre du personnel
        # return render(request, 'non_staff_template.html')
        return redirect('homepage.html')  # template à crer et à modifier


def admin_logout(request):
    return redirect(homepage)
    # return LogoutView.as_view()(request)


# ---------------------------------------------------------------------------------
# ------------------------ DOCTOR RELATED VIEWS START -----------------------------
# ---------------------------------------------------------------------------------
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
                # message = f'Hello, {user.username}! You are connected successfully.'
                return redirect('doctor_workspace')
            else:
                message = 'Invalid identifier or password'
    return render(
        request, 'doctor_login.html', context={'form': form, 'message': message})


@login_required
def doctor_workspace(request):
    # 计算 bed_occupied 和 operating_room_occupied 的信息
    total_beds = Bed.objects.count()
    occupied_beds = Bed.objects.exclude(id_patient=None).count()
    bed_occupied = (occupied_beds / total_beds) * 100 if total_beds > 0 else 0

    total_operating_rooms = OperatingRoom.objects.count()
    occupied_operating_rooms = OperatingRoomSchedule.objects.count()
    operating_room_occupied = (
                                          occupied_operating_rooms / total_operating_rooms) * 100 if total_operating_rooms > 0 else 0

    context = {
        'doctor': request.user.doctor,
        'bed_occupied': round(bed_occupied, 1),
        'operating_room_occupied': round(operating_room_occupied, 1),
    }

    return render(request, 'doctor_workspace.html', context)


@login_required
def add_patient(request):
    # return add(request, 'PatientForm', 'add_patient.html', 'doctor_workspace')
    if request.method == "POST":
        patient_form = PatientForm(request.POST)
        if patient_form.is_valid():
            # 保存病人信息
            patient = patient_form.save()

            # 获取选择的床位
            selected_bed = patient_form.cleaned_data.get('id_bed')

            if selected_bed:
                # 将床位关联到病人
                selected_bed.id_patient = patient
                selected_bed.save()

                # 更新BedForm中的id_patient字段
                bed_data = {'id_patient': patient.id_patient, 'id_department': selected_bed.id_department, 'bed_department': selected_bed.bed_department}
                bed_form = BedForm(data=bed_data)
                if bed_form.is_valid():
                    bed_form.save()

            return redirect('doctor_workspace')# 可以添加其他逻辑，比如在页面上显示成功消息

    else:
        patient_form = PatientForm()

    return render(request, 'add_patient.html', {'form': patient_form})

def discharge_patient(request, patient_id):
    # 获取要出院的病人
    patient = get_object_or_404(Patient, id=patient_id)

    # 获取病人所在的床位
    bed = patient.id_bed

    if bed:
        # 将床位关联到病人设为 None，表示空床位
        bed.id_patient = None
        bed.save()

        # 更新BedForm中的id_patient字段
        bed_data = {'id_patient': None, 'id_department': bed.id_department, 'bed_department': bed.bed_department}
        bed_form = BedForm(data=bed_data, instance=bed)
        if bed_form.is_valid():
            bed_form.save()

    # 删除病人
    patient.delete()

    return redirect('doctor_workspace')  # 重定向回医生工作区，或者你想要的其他页面
def my_operation(request):
    # 获取当前登录用户对应的医生对象
    current_doctor = request.user.doctor
    # 获取医生ID
    current_doctor_id = current_doctor.id_doctor
    # Operation of current doctor
    doctor_operations = OperatingRoomSchedule.objects.filter(id_doctor=current_doctor_id).values()
    data = list(doctor_operations)
    # return JsonResponse({'data': data})
    context = {'data': data}

    # context to render
    return render(request, 'my_operation.html', context)

# def my_patient(request):

@login_required
def add_operation(request):
    return add(request, 'OperationForm', 'add_operation.html', 'doctor_workspace')

def patients(request, ):
    patients = Patient.objects.all()
    return render(request, "patients.html", {"patients":  patients})


    # patients_list = Patient.objects.values(
    #     'id_bed', 'last_name', 'patient_department',
    #     'first_name', 'last_name', 'date_of_birth', 'gender_patient'
    # )
    # return JsonResponse(list(patients_list), safe=False)
    # return JsonResponse(data, safe=False)

# def patients(request):
#     patients_list = Patient.objects.all()
#     serializer = PatientSerializer(patients_list, many=True)
#     return JsonResponse(serializer.data, safe=False)


@login_required
def operating_room_booking(request):
    return add(request, 'OperatingRoomScheduleForm', 'operating_room_booking.html', 'doctor_workspace')


def doctor_logout(request):
    return redirect(homepage)

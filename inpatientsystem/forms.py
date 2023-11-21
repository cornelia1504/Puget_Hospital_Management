
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from inpatientsystemApp.models import Department, Patient, Doctor, Bed, Operation, OperatingRoom, OperatingRoomSchedule, OperationPerforming
from django.contrib.auth.forms import UserCreationForm
#login admin/doctor
class admin_login_Form(forms.Form):
    username = forms.CharField(max_length=63, label='Username')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Password')

class doctor_login_Form(forms.Form):
    username = forms.CharField(max_length=63, label='Username')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Password')


# for admin signup

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        widgets = {
            'password': forms.PasswordInput()
        }

class SuperuserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'is_staff', 'is_superuser')

class DoctorUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class DoctorForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = ['name_department', 'first_name', 'last_name', 'description_doctor']

# for patient related form
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['id_bed', 'id_doctor', 'id_department', 'first_name', 'last_name', 'date_of_birth', 'patient_department', 'gender_patient']

# for bed related form
class BedForm(forms.ModelForm):
    class Meta:
        model = Bed
        fields = ['id_patient', 'id_department', 'bed_department']

# for operation related form
class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = ['id_operating_room', 'id_patient', 'name_operation', 'date_of_operation']

# for operating room related form
class OperatingRoomForm(forms.ModelForm):
    class Meta:
        model = OperatingRoom
        fields = ['class_operating_room']

# for operating room schedule related form
class OperatingRoomScheduleForm(forms.ModelForm):

    class Meta:
        model = OperatingRoomSchedule
        fields = ['id_doctor', 'id_operating_room', 'scheduled_time', 'finish_time']

# for operation performing related form
class OperationPerformingForm(forms.ModelForm):
    class Meta:
        model = OperationPerforming
        fields = ['id_doctor', 'id_operation', 'id_patient', 'name_operation', 'date_of_operation']

# for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class DoctorSignupForm(UserCreationForm):
    name_department = forms.CharField(max_length=50, required=True)
    description_doctor = forms.CharField(required=True, widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        doctor = Doctor.objects.create(
            user=user,
            name_department=self.cleaned_data['name_department'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            description_doctor=self.cleaned_data['description_doctor']
        )
        return user
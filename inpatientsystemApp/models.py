# models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Department(models.Model):
    id_department = models.AutoField(primary_key=True)
    name_department = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name_department

class Patient(models.Model):
    id_patient = models.AutoField(primary_key=True)
    id_bed = models.ForeignKey('Bed', on_delete=models.SET_NULL, null=True)
    id_doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True)
    id_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    patient_department = models.CharField(max_length=50)
    gender_patient = models.CharField(max_length=10)

class Doctor(models.Model):
    id_doctor = models.AutoField(primary_key=True)
    name_department = models.ForeignKey(Department, on_delete=models.CASCADE, to_field='name_department')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, null=True)
    description_doctor = models.TextField()
    profile_pic = models.ImageField(upload_to='doctor_profile_pic/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor', null=True, blank=True)
class Bed(models.Model):
    id_bed = models.AutoField(primary_key=True)
    id_patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    id_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    bed_department = models.CharField(max_length=50)


class Operation(models.Model):
    id_operation = models.AutoField(primary_key=True)
    id_operating_room = models.ForeignKey('OperatingRoom', on_delete=models.CASCADE)
    id_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name_operation = models.CharField(max_length=50)
    date_of_operation = models.DateField()

class OperatingRoom(models.Model):
    id_operating_room = models.AutoField(primary_key=True)
    class_operating_room = models.CharField(max_length=50)



class OperatingRoomSchedule(models.Model):
    id_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    id_operating_room = models.ForeignKey(OperatingRoom, on_delete=models.CASCADE)
    class_operating_room = models.CharField(max_length=50)
    scheduled_time = models.DateTimeField()
    finish_time = models.DateTimeField()

    constraints = [
        models.CheckConstraint(
            check=(
                    models.Q(id_operating_room__class_operating_room='C',
                             scheduled_time__iso_week_day__in=[1, 2, 3, 4, 5],
                             scheduled_time__hour__gte=8,
                             scheduled_time__hour__lt=16,
                             finish_time__hour__lte=16) |
                    models.Q(id_operating_room__class_operating_room='B',
                             scheduled_time__hour__gte=8,
                             finish_time__hour__lte=20) |
                    models.Q(id_operating_room__class_operating_room='A',
                             scheduled_time__hour__gte=0,
                             finish_time__hour__lte=24)
            ),
            name='valid_scheduling_time'
        )
    ]


class OperationPerforming(models.Model):
    id_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    id_operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    id_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name_operation = models.CharField(max_length=50)
    date_of_operation = models.DateField()

    def __str__(self):
        return f'{self.name_operation} - {self.date_of_operation}'

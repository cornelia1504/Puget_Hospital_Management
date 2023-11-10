from django.db import models

class Department(models.Model):
    id_department = models.AutoField(primary_key=True)
    name_department = models.CharField(max_length=50)

class Patient(models.Model):
    id_patient = models.AutoField(primary_key=True)
    id_bed = models.ForeignKey('Bed', on_delete=models.SET_NULL, null=True)
    id_doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True)
    id_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    nom_patient = models.CharField(max_length=50)
    prenom_patient = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    patient_department = models.CharField(max_length=50)
    gender_patient = models.CharField(max_length=10)

class Doctor(models.Model):
    id_doctor = models.AutoField(primary_key=True)
    id_department = models.ForeignKey(Department, on_delete=models.CASCADE)
    nom_doctor = models.CharField(max_length=50)
    prenom_doctor = models.CharField(max_length=50)
    description_doctor = models.TextField()

class Bed(models.Model):
    id_bed = models.AutoField(primary_key=True)
    id_patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    id_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    bed_department = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to='doctor_profile_pic/', null=True, blank=True)

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

class OperationPerforming(models.Model):
    id_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    id_operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    id_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name_operation = models.CharField(max_length=50)
    date_of_operation = models.DateField()

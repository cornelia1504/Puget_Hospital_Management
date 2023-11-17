from django.contrib import admin
from inpatientsystemApp.models import Department, Patient, Doctor, Bed, Operation, OperatingRoom, OperatingRoomSchedule, OperationPerforming

admin.site.register(Department)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Bed)
admin.site.register(Operation)
admin.site.register(OperatingRoom)
admin.site.register(OperatingRoomSchedule)
admin.site.register(OperationPerforming)
# Register your models here.


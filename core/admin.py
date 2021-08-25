from django.contrib import admin

from .models import Triagem, User, Role, Employee, Patient, Attendance, VitalData

@admin.register(Employee)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', "last_name", "created_at", "email", "role", "conselho")

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['cod',]

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', "birth_date", "cns", "cpf", "gender", "city", "uf", "street", "neighborhood", "num")

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('patient', 'num', 'status', 'moment_triagem', 'moment_consultorio', 'moment_encerramento')

@admin.register(VitalData)
class VitalData(admin.ModelAdmin):
    list_display = ('temperature', 'pas', 'pad', 'saturation', 'heart_beats')

@admin.register(Triagem)
class TriagemAdmin(admin.ModelAdmin):
    list_display = ('attendance', 'responsible', 'vital_data', 'description', 'priority')
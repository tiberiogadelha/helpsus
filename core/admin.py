from django.contrib import admin

from .models import User, Role, Employee, Patient

@admin.register(Employee)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', "last_name", "created_at", "email", "role", "conselho")

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['cod',]

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', "birth_date", "cns", "cpf", "gender", "city", "uf", "street", "neighborhood", "num")



# Register your models here.

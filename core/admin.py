from django.contrib import admin

from .models import User, Role

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', "created_at", "email", "role", "conselho")

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['cod']


# Register your models here.

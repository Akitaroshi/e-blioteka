from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Добавляем наши новые поля в интерфейс админки
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('full_name', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('full_name', 'phone')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
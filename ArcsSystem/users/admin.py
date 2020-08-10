# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'email',
        'username',
        'date_joined',
        'accepted_eula',
        'accepted_eula_version',
        'accepted_eula_date',
        'is_staff',
        'is_active'
        ]

admin.site.register(CustomUser, CustomUserAdmin)

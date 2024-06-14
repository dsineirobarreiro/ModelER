from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.conf import settings

from .models import User
from .forms import SignupForm



class CustomUserAdmin(UserAdmin):
    add_form = SignupForm
    form = SignupForm
    model = settings.AUTH_USER_MODEL
    list_display = ("username", "email", "is_staff", "is_active","last_login", "date_joined")
    list_filter = ("username", "email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
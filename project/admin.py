from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Company, Employee, Request, RequestImage


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    list_display = ("phone_number", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("phone_number", "first_name", "last_name")
    ordering = ("phone_number",)

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "image", "region", "district", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )


admin.site.register(Company)
admin.site.register(Request)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Company, Employee, Request, RequestImage


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    list_display = ("phone_number", "first_name", "last_name", "is_staff", "is_active", "passport")
    search_fields = ("phone_number", "first_name", "last_name", "passport")
    ordering = ("phone_number",)

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "image", "region", "district", "role", "passport")}),
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


class RequestImageInline(admin.TabularInline):
    model = RequestImage
    extra = 1


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ["pk", "company", "employee", "priority", "description", "long", "lat", "status", "get_images_count"]
    inlines = [RequestImageInline]
    list_display_links = ["pk", "company"]

    def get_images_count(self, obj):
        return obj.images.all().count()

    get_images_count.description = "Images Count"


admin.site.register(Company)

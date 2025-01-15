from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import OTP, Company, Employee, Request, RequestImage


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


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "stir", "phone_number", "status", "region", "district"]
    list_filter = ["stir", "phone_number"]
    list_editable = ["phone_number"]


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ["id", "company", "code", "phone_number", "is_active"]
    actions = ["clear_expired_otp"]

    def phone_number(self, obj):
        return obj.company.phone_number

    def is_active(self, obj):
        return not obj.is_expired()

    phone_number.description = "Phone number"
    is_active.boolean = True

    @admin.action(description="Clear expired OTPs")
    def clear_expired_otp(self, request, queryset):
        expired_items = [obj for obj in queryset if obj.is_expired()]

        for obj in expired_items:
            obj.delete()

        self.message_user(request, f"{len(expired_items)} expired OTPs have been cleared.")

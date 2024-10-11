from django.contrib import admin

from .models import Company, Employee, Request, RequestImage


admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(Request)
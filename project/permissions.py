from rest_framework.permissions import BasePermission


class CompanyIsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.company)

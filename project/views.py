import django_filters
from django.shortcuts import render
from rest_framework import decorators, mixins, permissions, status, viewsets
from rest_framework.response import Response

from .models import Company, Employee, Request, RequestImage
from .serializers import CompanySerializer, EmployeeSerializer, RequestSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAdminUser]

    @decorators.action(methods=["GET"], detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_me(self, request, *args, **kwargs):
        return Response(self.get_serializer(self.request.user).data, status=status.HTTP_200_OK)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ["stir"]


class RequestsViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    filterset_fields = ["employee"]

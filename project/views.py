from django.shortcuts import render

from rest_framework import viewsets

from .models import Company, Request, Employee, RequestImage
from .serializers import EmployeeSerializer, CompanySerializer, RequestSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class RequestsViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
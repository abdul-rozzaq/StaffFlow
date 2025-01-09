import django_filters
from django.shortcuts import render
from rest_framework import decorators, mixins, permissions, status, viewsets
from rest_framework.response import Response

from .models import Company, Employee, Request, RequestImage
from .serializers import CompanySerializer, EmployeeSerializer, RequestSerializer


class EmployeeViewSet(viewsets.GenericViewSet, mixins.DestroyModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin):
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


class RequestsViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["employee"]

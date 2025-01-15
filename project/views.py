import random

from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now
from rest_framework import decorators, mixins, permissions, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .models import OTP, Company, Employee, Request, RequestImage
from .permissions import CompanyIsAuthenticated
from .serializers import *
from .utils import generate_token_for_company, send_otp_code


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAdminUser]
    # parser_classes = [FormParser, MultiPartParser]

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


class CompanyAuthenticationViewSet(viewsets.GenericViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_serializer_class(self):
        serializer_classes = {
            "send_otp": StirAuthenticationSerializer,
            "verify_otp": PhoneNumberOTPSerializer,
        }
        return serializer_classes[self.action] if self.action in serializer_classes else self.serializer_class

    @decorators.action(["POST"], detail=False)
    def send_otp(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()

        stir = serializer.validated_data["stir"]

        company = get_object_or_404(Company, stir=stir)
        otp_code = str(random.randint(100000, 999999))

        if company.phone_number:
            otp, created = OTP.objects.update_or_create(company=company, defaults={"code": otp_code, "created_at": now()})

            send_otp_code(number=company.phone_number, code=otp_code)

            return Response({"message": "Tasdiqlash kodi muvaffaqqiyatli yuborildi"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Kompaniyaga telefon raqam biriktirilmagan"}, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(["POST"], detail=False)
    def verify_otp(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number, code = serializer.validated_data["phone_number"], serializer.validated_data["otp"]

        try:
            company = Company.objects.get(phone_number=phone_number)
            otp = OTP.objects.get(company=company, code=code)
        except (Company.DoesNotExist, OTP.DoesNotExist):
            return Response({"detail": "Telefon raqami yoki OTP kodi noto'g'ri."}, status=status.HTTP_400_BAD_REQUEST)

        if otp.is_expired():
            return Response({"detail": "OTP kodi muddati tugagan."}, status=status.HTTP_400_BAD_REQUEST)

        otp.delete()

        token = generate_token_for_company(company)

        return Response(
            {
                "message": "asdasdasd",
                "token": token,
                "company": CompanySerializer(company, context={"request": request}).data,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["GET"])
@decorators.permission_classes([CompanyIsAuthenticated])
def test(request):
    print(request.company)
    return Response({"message": "success"})

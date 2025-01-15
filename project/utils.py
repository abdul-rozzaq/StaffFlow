from django.conf import settings
from .models import Company, CompanyToken


def send_otp_code(number: str, code: int):
    # if settings.DEBUG:
    # return print(f"{number}: {code}")

    return print(f"{number}: {code}")


def generate_token_for_company(company):
    token, created = CompanyToken.objects.get_or_create(company=company)
    return token.key

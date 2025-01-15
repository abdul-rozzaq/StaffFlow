from django.utils.deprecation import MiddlewareMixin

from .models import Company, CompanyToken


class CompanyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")

        if token:
            try:
                token_key = token.split()[1]
                token_obj = CompanyToken.objects.get(key=token_key)
                company = Company.objects.get(pk=token_obj.company_id)

                request.company = company
            except (CompanyToken.DoesNotExist, Company.DoesNotExist):
                request.company = None
        else:
            request.company = None

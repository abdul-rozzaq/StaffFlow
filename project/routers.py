from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, CompanyViewSet, RequestsViewSet


router = DefaultRouter()

router.register("employees", EmployeeViewSet)
router.register("companies", CompanyViewSet)
router.register("requests", RequestsViewSet)

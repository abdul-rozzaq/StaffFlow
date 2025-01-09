from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class EmployeeManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Oddiy foydalanuvchi yaratish funksiyasi.
        """
        if not phone_number:
            raise ValueError("The phone number must be provided")
        phone_number = self.normalize_phone_number(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Superuser yaratish funksiyasi.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)

    def normalize_phone_number(self, phone_number):
        """
        Telefon raqamni normalizatsiya qilish uchun (masalan, +998 formatida).
        """
        return phone_number.strip().replace(" ", "")


class Employee(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(default="images/default-user.png", upload_to="employee-images", blank=True, null=True)

    region = models.CharField(max_length=128)
    district = models.CharField(max_length=128)

    role = models.CharField(choices=(("director", "DIRECTOR"), ("manager", "MANAGER"), ("employee", "EMPLOYEE")), max_length=128, blank=True, null=True)
    position = models.CharField(max_length=128, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = EmployeeManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def full_name(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.phone_number

    def __str__(self):
        return self.full_name()


class Company(models.Model):
    name = models.CharField(max_length=255)
    stir = models.CharField(max_length=64)
    address = models.TextField()
    status = models.CharField(max_length=16)

    region = models.CharField(max_length=128)
    district = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name


class Request(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    priority = models.IntegerField()
    description = models.TextField()
    long = models.CharField(max_length=256)
    lat = models.CharField(max_length=256)
    file = models.FileField(blank=True)
    status = models.CharField(
        choices=(
            ("pending", "PENDING"),
            ("accepted", "ACCEPTED"),
            ("rejected", "REJECTED"),
            ("on_going", "ON_GOING"),
        ),
        max_length=150,
        default="accepted",
    )

    def __str__(self):
        return self.pk


class RequestImage(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="request-images/")

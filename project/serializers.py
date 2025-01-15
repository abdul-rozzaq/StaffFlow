from rest_framework import serializers

from .models import Company, Employee, Request, RequestImage


class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ["id", "image", "first_name", "last_name", "role", "phone_number", "region", "district", "password", "passport", "image"]

    def create(self, validated_data):
        employee: Employee = super().create(validated_data)
        employee.is_active = True
        employee.set_password(validated_data["password"])
        employee.save()

        return employee

    def update(self, instance, validated_data):
        password = validated_data.get("password")

        employee: Employee = super().update(instance, validated_data)

        if password:
            employee.set_password(password)
            employee.save()

        return employee


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "stir", "status", "region", "district", "phone_number"]


class RequestSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(allow_empty_file=False), write_only=True, required=True)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = Request
        fields = ["id", "employee", "company", "priority", "description", "long", "lat", "file", "images", "status"]

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["employee"] = request.user

        images = validated_data.pop("images")
        created_request = super().create(validated_data)

        for img in images:
            RequestImage.objects.create(request=created_request, image=img)

        return created_request

    def update(self, instance, validated_data):
        images = validated_data.pop("images", [])

        if images:
            instance.images.all().delete()

            for img in images:
                RequestImage.objects.create(request=instance, image=img)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serialized_data = super().to_representation(instance)
        serialized_data["company"] = CompanySerializer(instance.company).data
        serialized_data["images"] = [self.context["request"].build_absolute_uri(img.image.url) for img in instance.images.all()]
        return serialized_data


class RequestImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestImage
        fields = ["id", "request", "image"]


class StirAuthenticationSerializer(serializers.Serializer):
    stir = serializers.CharField()

class PhoneNumberOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.IntegerField()
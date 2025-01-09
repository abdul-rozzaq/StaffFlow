from rest_framework import serializers

from .models import Company, Employee, Request, RequestImage


class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    region = serializers.CharField(read_only=True)
    district = serializers.CharField(read_only=True)

    class Meta:
        model = Employee
        fields = ["id", "image", "first_name", "last_name", "role", "phone_number", "region", "district", "password"]


class CompanySerializer(serializers.ModelSerializer):
    region = serializers.CharField(read_only=True)
    district = serializers.CharField(read_only=True)

    class Meta:
        model = Company
        fields = ["id", "name", "stir", "address", "status", "region", "district"]


class RequestSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(allow_empty_file=False), write_only=True)

    employee = EmployeeSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Request
        fields = ["id", "employee", "company", "priority", "description", "long", "lat", "file", "images", "status"]

    def create(self, validated_data):
        images = validated_data.pop("images")
        request = super().create(validated_data)

        for img in images:
            RequestImage.objects.create(request=request, image=img)

        return request

    def to_representation(self, instance):
        """
        JSON formatdagi javobni o'zgartirish uchun.
        """
        serialized_data = super().to_representation(instance)

        serialized_data["images"] = [self.context["request"].build_absolute_uri(img.image.url) for img in instance.images.all()]
        serialized_data["employee"] = EmployeeSerializer(instance.employee, context=self.context).data
        serialized_data["company"] = CompanySerializer(instance.company, context=self.context).data

        return serialized_data


class RequestImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestImage
        fields = ["id", "request", "image"]

from rest_framework import serializers

from .models import Company, Request, Employee, RequestImage


class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "image",
            "first_name",
            "last_name",
            "role",
            "phone_number",
            "address",
            "password",
        ]


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ["id", "name", "stir", "address", "status"]


class RequestSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False), write_only=True
    )

    class Meta:
        model = Request
        fields = [
            "id",
            "employee",
            "company",
            "priority",
            "description",
            "long",
            "lat",
            "file",
            "images",
        ]

    def create(self, validated_data):
        images = validated_data.pop("images")

        request = super().create(validated_data)

        for img in images:
            RequestImage.objects.create(request=request, image=img)

        return request

    def to_representation(self, instance):
        serialized_data = super().to_representation(instance)

        serialized_data["images"] = [self.context['request'].build_absolute_uri(img.image.url) for img in instance.images.all()]

        return serialized_data

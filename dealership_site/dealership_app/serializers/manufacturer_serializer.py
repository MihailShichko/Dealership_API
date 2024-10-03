from rest_framework import serializers

from ..models.manufacturer import Manufacturer


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'
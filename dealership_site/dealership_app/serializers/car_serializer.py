from rest_framework import serializers

from .manufacturer_serializer import ManufacturerSerializer
from ..models.car import Car
from ..models.manufacturer import Manufacturer

class CarReadSerializer(serializers.ModelSerializer):
    cat = ManufacturerSerializer()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model= Car
        fields = ("id", "name", "manufacture_date", "price", "horsepower", "cat", "user")


class CarWriteSerializer(serializers.ModelSerializer):
    cat = serializers.PrimaryKeyRelatedField(queryset=Manufacturer.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Car
        fields = ("id", "name", "manufacture_date", "price", "horsepower", "cat", "user")
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

    def create(self, validated_data):
        group_name = validated_data.pop("group")
        user = User.objects.create(**validated_data)

        group = Group.objects.get(group_name)
        group.users.add(user)

        return user
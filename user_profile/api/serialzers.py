from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class UserCreateSerializer(ModelSerializer):
    password = CharField(required=True, write_only=True)
    confirm_password = CharField(required=True, write_only=True)
    username = CharField(required=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "confirm_password",
        )

    def validate(self, data):
        user = User.objects.filter(username=data["username"]).first()
        if user:
            raise ValidationError({"username": "This user has already created"})
        if data["password"] != data["confirm_password"]:
            raise ValidationError({"confirm_password": "The password and confirm password don't match."})
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        validated_data["password"] = make_password(validated_data["password"])
        super().create(validated_data)
        user = User.objects.filter(username=validated_data["username"]).first()
        return user


class UserAuthSerializer(ModelSerializer):
    username = CharField(required=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }


class UserActivitySerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'last_login',
            'last_request',
        )

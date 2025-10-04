from rest_framework import serializers

from .models import User


class UserSerializeer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    avatar = serializers.ImageField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "avatar"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        for field in ["email", "avatar", "password"]:
            if field in validated_data:
                if field == "password":
                    instance.set_password(validated_data["password"])
                else:
                    setattr(instance, field, validated_data[field])

        instance.save()            
        return instance

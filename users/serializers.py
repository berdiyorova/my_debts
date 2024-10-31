from rest_framework import serializers

from users.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=16)

    class Meta:
        model = UserModel
        fields = ('username', 'phone_number', 'password', 'confirm_password')

    def validate_password(self, value):
        if value != self.confirm_password:
            raise serializers.ValidationError("Password and confirm_password do not match")
        return value

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password before creating the user
        user = UserModel(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

from rest_framework import serializers

from users.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=16)

    class Meta:
        model = UserModel
        fields = ('username', 'phone_number', 'password')

    def validate_password(self, value):
        if value != self.confirm_password:
            raise serializers.ValidationError("Password and confirm_password do not match")
        return value

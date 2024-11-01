from rest_framework import serializers

from users.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=16, write_only=True)

    class Meta:
        model = UserModel
        fields = ('username', 'phone_number', 'password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] != attrs.get('confirm_password'):
            raise serializers.ValidationError({"password": "Password and confirm_password do not match."})
        return attrs

    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data['username'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

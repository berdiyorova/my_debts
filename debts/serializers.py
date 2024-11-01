from rest_framework import serializers

from debts.models import DebtModel, CurrencyModel
from users.models import UserModel


class DebtSerializer(serializers.ModelSerializer):
    status = serializers.CharField(max_length=64, required=False)
    lender = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all(), required=False)
    borrower = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all(), required=False)
    currency = serializers.PrimaryKeyRelatedField(queryset=CurrencyModel.objects.all(), required=False)

    class Meta:
        model = DebtModel
        fields = ('id', 'amount', 'currency', 'lender', 'borrower', 'status')

    def update(self, instance, validated_data):
        pass

    def to_representation(self, instance):
        """Convert the model instance to a dictionary for representation."""
        data = super().to_representation(instance)

        data['status_display'] = instance.get_status_display()  # Get human-readable status

        # Optionally, you can add additional fields or modify existing ones

        data['currency_code'] = instance.currency.code if data['currency'] else None

        data['lender'] = {
            'username': instance.lender.username,
            'phone_number': instance.lender.phone_number
        }
        data['borrower'] = {
            'username': instance.borrower.username,
            'phone_number': instance.borrower.phone_number
        }

        # Remove original currency field if you only want to show transformed data
        data.pop('currency', None)

        return data

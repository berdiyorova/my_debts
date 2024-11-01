from decimal import Decimal

from rest_framework import serializers

from debts.models import DebtModel, CurrencyModel
from users.models import UserModel


class DebtSerializer(serializers.ModelSerializer):
    lender = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all(), required=False)
    borrower = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all(), required=False)
    currency = serializers.PrimaryKeyRelatedField(queryset=CurrencyModel.objects.all(), required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    remaining_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = DebtModel
        fields = ('id', 'amount', 'last_paid_amount', 'remaining_amount', 'currency', 'lender', 'borrower', 'status')

    def create(self, validated_data):
        debt = DebtModel.objects.create(**validated_data)
        debt.remaining_amount = debt.amount
        debt.save()
        return debt

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if validated_data['last_paid_amount']:
            instance.remaining_amount -= instance.last_paid_amount

        if instance.remaining_amount <= 0:
            instance.status = instance.Status.PAID

        instance.save()
        return instance

    def __delete__(self, instance):
        instance.status = instance.Status.DELETED
        instance.save()
        return instance

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

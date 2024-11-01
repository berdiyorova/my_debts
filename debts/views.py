from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from debts.serializers import DebtSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def lend_view(request):
    if request.method == 'POST':
        serializer = DebtSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['lender'] = request.user
        instance = serializer.save()
        return Response(data=DebtSerializer(instance=instance).data, status=status.HTTP_201_CREATED)

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from debts.models import DebtModel
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def borrow_view(request):
    if request.method == 'POST':
        serializer = DebtSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['borrower'] = request.user
        instance = serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_borrowed_debts(request):
    if request.method == 'GET':
        debts = DebtModel.objects.filter(borrower=request.user)
        serializer = DebtSerializer(debts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_lent_debts(request):
    if request.method == 'GET':
        debts = DebtModel.objects.filter(lender=request.user)
        serializer = DebtSerializer(debts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

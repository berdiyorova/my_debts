from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.views import get_page_and_page_size
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

        search = request.query_params.get('search')
        page, page_size = get_page_and_page_size(request)

        if search is not None:
            debts = DebtModel.objects.filter(
                Q(lender__username__icontains=search) | Q(lender__phone_number__icontains=search)
            )

        page -= 1
        debts = debts[page * page_size: page * page_size + page_size]

        serializer = DebtSerializer(debts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_lent_debts(request):
    if request.method == 'GET':
        debts = DebtModel.objects.filter(lender=request.user)

        search = request.query_params.get('search')
        page, page_size = get_page_and_page_size(request)

        if search is not None:
            debts = DebtModel.objects.filter(
                Q(borrower__username__icontains=search) | Q(borrower__phone_number__icontains=search)
            )

        page -= 1
        debts = debts[page * page_size: page * page_size + page_size]

        serializer = DebtSerializer(debts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def debt_detail(request, pk):
    debt = get_object_or_404(DebtModel, pk=pk)

    if request.method == 'GET':
        serializer = DebtSerializer(debt)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = DebtSerializer(instance=debt, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    elif request.method == 'PATCH':
        serializer = DebtSerializer(instance=debt, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    elif request.method == 'DELETE':
        debt.delete()
        return Response(data={'success': True}, status=status.HTTP_204_NO_CONTENT)

from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from common.views import get_page_and_page_size
from users.models import UserModel
from users.serializers import UserSerializer


@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_detail_view(request, pk):
    user = get_object_or_404(UserModel, pk=pk)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = UserSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    elif request.method == 'PATCH':
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def users_list(request):
    if request.method == 'GET':
        users = UserModel.objects.all()

        search = request.query_params.get('search')
        page, page_size = get_page_and_page_size(request)

        if search is not None:
            users = UserModel.objects.filter(Q(username__icontains=search) | Q(phone_number__icontains=search))

        page -= 1
        users = users[page * page_size: page * page_size + page_size]

        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_detail_view(request, pk):
    user = get_object_or_404(UserModel, pk=pk)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        user.delete()
        return Response(data={'success': True}, status=status.HTTP_204_NO_CONTENT)

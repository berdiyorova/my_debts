from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', obtain_auth_token, name='register'),
    path('<int:pk>/', views.user_detail_view, name='user_detail'),
    path('admin/<int:pk>/', views.admin_detail_view, name='admin_detail'),
]

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

class UserModel(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True, blank=False)
    phone_number = models.CharField(max_length=20)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

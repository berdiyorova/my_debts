from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

class UserModel(AbstractBaseUser):
    phone_number = models.CharField(max_length=20)

from django.contrib.auth.models import AbstractUser
from django.db import models

from Manager.models import Playlist


class User(AbstractUser):
    REQUIRED_FIELDS = ('email', 'first_name', 'last_name', 'password')

    class Meta:
        db_table = "User"

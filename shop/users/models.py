from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Mate:
        db_table = 'user'

    def __str__(self):
        return self.username
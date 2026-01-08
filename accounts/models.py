from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = "CLIENT", "Client"
        STAFF = "STAFF", "Staff"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT)

    def is_client(self) -> bool:
        return self.role == self.Role.CLIENT

    def is_staff_user(self) -> bool:
        return self.role == self.Role.STAFF

    def is_admin_user(self) -> bool:
        return self.role == self.Role.ADMIN

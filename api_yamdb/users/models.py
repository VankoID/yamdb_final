from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    ]
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150,
                                  blank=True, default="first name")
    last_name = models.CharField(max_length=150, blank=True,
                                 default="last name")
    bio = models.TextField(blank=True, default="bio")
    role = models.CharField(max_length=15, choices=ROLES_CHOICES, default=USER)
    confirmation_code = models.CharField(max_length=255,
                                         blank=True, default='12233')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

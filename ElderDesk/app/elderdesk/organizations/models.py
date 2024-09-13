from django.db import models
import uuid
from django.conf import settings

class Organization(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255, unique=True)
    domains = models.TextField(help_text="List of domains separated by spaces")
    optional_info = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def add_user(self, name, email, user_type):
        if UserProfile.objects.filter(email=email).exists():
            return None, False
        user_profile = UserProfile.objects.create(
            organization=self,
            name=name,
            email=email,
            user_type=user_type
        )
        return user_profile, True

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('end_user', 'End User'),
        ('staff', 'Staff'),
    ]

    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='user_profiles')
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.email})'

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
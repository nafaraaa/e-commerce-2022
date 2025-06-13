from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified=models.BooleanField(default=False)
    verification_code=models.CharField(max_length=6, blank=True, null=True)
    code_created_at=models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"
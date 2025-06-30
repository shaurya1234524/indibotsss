from django.db import models

# Create your models here.
# projects/models.py
from django.db import models
from django.contrib.auth.models import User
import secrets
import string

def generate_bot_key():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

class Project(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    bot_key = models.CharField(max_length=64, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.bot_key:
            self.bot_key = generate_bot_key()
        super().save(*args, **kwargs)


class QuestionAnswer(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='qas')
    question = models.CharField(max_length=255)
    answer = models.TextField(blank=True)
    image = models.ImageField(upload_to='answers/', blank=True, null=True)
    image_description = models.CharField(max_length=255, blank=True, null=True)  # ✅ optional

from django.contrib.auth.models import User
import random

class OTPVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()
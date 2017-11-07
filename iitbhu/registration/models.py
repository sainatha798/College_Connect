from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Userinfo(models.Model):
    mobile_no = models.CharField(max_length=12)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True)
    profile_picture = models.FileField(default=None, null=True)
    dob = models.DateField(null=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('index')
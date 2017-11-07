from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Messages(models.Model):
    sender = models.ForeignKey(User,blank=True,null=True,)
    sender_del = models.BooleanField(default=False)
    sender_trash = models.BooleanField(default=False)
    mail_sub = models.CharField(null=True,blank=True,max_length=100)
    mail_body = models.TextField(null=True,blank=True)
    receiver = models.ForeignKey(User,related_name='mail')
    receiver_del = models.BooleanField(default=False,blank=True)
    receiver_trash = models.BooleanField(default=False,blank=True)
    is_read = models.BooleanField(default=False,blank=True)
    file = models.FileField(default=None,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sender.username + self.mail_sub + self.receiver.username

    def get_absolute_url(self):
        return reverse('messaging:encrypt',kwargs={'pk':self.pk})


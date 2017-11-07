from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Post(models.Model):
    text = models.TextField(default=None,null=True,blank=True)
    pic = models.FileField(default=None,null=True,blank=True)
    video = models.FileField(default=None, null=True,blank=True)

    post_file = models.FileField(default=None, null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    likes = models.PositiveIntegerField(default=0)
    tag_no = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('postfeed:addPostTag', kwargs={'pk':self.pk})


    def __str__(self):
        if self.user==None:
            return str(self.pk)
        else:
            return self.user.username + str(self.pk)


class Tag(models.Model):
    tag = models.CharField(max_length=100)
    post = models.ManyToManyField(Post, symmetrical=True, blank=True,null=True,default=None)

    def __str__(self):
        return self.tag


class UserPrefernces(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    tags = models.ManyToManyField(Tag, symmetrical=True, blank=True,null=True,default=None)

    def __str__(self):
        return self.user.username
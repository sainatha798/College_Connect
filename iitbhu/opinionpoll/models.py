from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class PollQuestion(models.Model):
    poll_question = models.TextField()
    no_of_choices = models.PositiveIntegerField(default=2)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    voted = models.ManyToManyField(User,symmetrical=True,null=True,blank=True,default=None,related_name='voted')
    def get_absolute_url(self):
        return reverse('opinionpoll:add_choice', kwargs={'pk':self.pk})
    def __str__(self):
        return self.poll_question

class PollChoice(models.Model):
    poll_choice = models.CharField(max_length=500)
    poll_count = models.IntegerField(default=0)
    question = models.ForeignKey(PollQuestion,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return  self.poll_choice


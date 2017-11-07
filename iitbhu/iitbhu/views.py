__author__ = 'sainatha798'
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.conf import settings

def welcome(request):

    return HttpResponse(render(request,'registration/homepage.html'))

@login_required()
def index(request):
    user = request.user
    return HttpResponse(render(request,'registration/login_home.html' , {'user':user}))

@login_required()
def test(request):
    mail = request.user.email
    user1 = request.user
    count = User.objects.all().filter(email=mail).count()
    ##if count == 2:

    ##logout(request)
    user1.delete()

    try:
        user = User.objects.all().filter(email=mail)[0]
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request,user)
        return redirect(reverse('index'))
    except:
        ##return HttpResponse(mail)
    ##return HttpResponse(user.username)
        return HttpResponse(render(request,'registration/error.html'))
    ##return HttpResponse(request.user.email)


def credits(request):
    if request.user.is_authenticated():
        return HttpResponse(render(request,'registration/credits.html'))
    else:
        return HttpResponse(render(request, 'registration/credit.html'))
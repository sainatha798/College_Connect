from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from .import models
from django.db.models import Q
from Crypto.Cipher import AES
from .encrypt import secret_key, iv
import base64
from django.views.generic.edit import CreateView

# Create your views here.
@login_required()
def index(request):
    return HttpResponse(render(request, 'messaging/home.html'))

@login_required()
def inbox(request):
    user = request.user
    messages = models.Messages.objects.filter(receiver=user, receiver_trash=False)
    count = messages.count()
    return HttpResponse(render(request,'messaging/mail.html',{'messages':messages,'count':count}))

@login_required()
def outbox(request):
    user = request.user
    messages = models.Messages.objects.filter(sender=user , sender_trash=False)
    count = messages.count()
    return HttpResponse(render(request, 'messaging/mail.html', {'messages': messages, 'count': count}))


@login_required()
def encrypt(request,pk):
    msg = models.Messages.objects.get(pk=pk)
    msg.sender = request.user
    msg.mail_body = enc(msg.mail_body)
    msg.save()
    return HttpResponseRedirect(reverse('messaging:index'))
@login_required()
def mail(request,pk):
    msg = models.Messages.objects.get(pk=pk)
    msg.is_read = True
    msg.save()
    text = dec(msg.mail_body)
    return HttpResponse(render(request,'messaging/mail_view.html', {'msg':msg,'text':text}))
class Compose(CreateView):
    model = models.Messages
    fields = ['receiver', 'mail_sub',  'mail_body', 'file']

@login_required()
def delete(request,pk):
    user = request.user
    msg = models.Messages.objects.get(pk=pk)
    if msg.sender == user:
        if msg.sender_trash == True:
            msg.sender_del = True
        else:
            msg.sender_trash = True
    elif msg.receiver == user:
        if msg.receiver_trash == True:
            msg.receiver_del = True
        else:
            msg.receiver_trash = True
    msg.save()
    return HttpResponseRedirect(reverse('messaging:index'))

@login_required()
def trash(request):
    user = request.user
    messages = models.Messages.objects.filter(Q(sender=user)&Q(sender_trash=True, sender_del=False) | Q(receiver=user)&Q(receiver_trash=True, receiver_del=False))
    count = messages.count()
    return HttpResponse(render(request, 'messaging/mail.html', {'messages': messages, 'count':count}))


def enc(msg):
    while len(msg)%16!=0:
        msg = msg + ' '
    text = msg.encode('iso-8859-15')
    aes = AES.new(secret_key,AES.MODE_CBC,iv)
    return aes.encrypt(text).decode('iso-8859-15')

def dec(msg):
    text = msg.encode('iso-8859-15')
    aes = AES.new(secret_key,AES.MODE_CBC,iv)
    return aes.decrypt(text).decode('iso-8859-15')

@login_required()
def undo(request,pk):
    user = request.user
    msg = models.Messages.objects.get(pk=pk)
    if msg.sender == user:
        msg.sender_trash = False
    elif msg.receiver == user:
        msg.receiver_trash = False
    msg.save()
    return HttpResponseRedirect(reverse('messaging:trash'))
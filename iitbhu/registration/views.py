from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from . import forms,tokens,models
from django.views.generic.edit import UpdateView
# Create your views here.


def login_view(request):
    form = forms.Login(request.POST)
    a = reverse('registration:login')
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('index'))
        else:
            c=1
            return HttpResponse(render(request,'form.html', {'form':form, 'form_id':a,'c':c}))
    else:
        form = forms.Login()
        return HttpResponse(render(request,'form.html', {'form': form, 'form_id': a}))

@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
def signup(request):
    form = forms.Signup(request.POST)
    a = reverse('registration:signup')

    if form.is_valid():
        ##if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
            ##return HttpResponse(render(request, 'form.html', {'form':form, 'form_id': a, 'error': 'passwords don`t match'}))
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        account_activation = tokens.Activate_user()
        ctx = {'user': user, 'domain':current_site.domain,'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': account_activation.make_token(user)}
        message = render_to_string('account_activation.html', {'user': user, 'domain':current_site.domain,'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': account_activation.make_token(user)})
        message = get_template('account_activation.html').render(ctx)
        subject = 'Activate Your IITBHU Connect Account'
        sender = form.cleaned_data['email']
        try:
            msg = EmailMessage(subject, message, to=[sender])
            msg.content_subtype = 'html'
            msg.send()
        except:
            user.delete()
            form = forms.Signup()
            return HttpResponse(render(request, 'form.html', {'form': form, 'form_id': a}))
        return HttpResponseRedirect(reverse('registration:profile', kwargs={'pk': user.pk}))
    else:
        try:
            form = forms.Signup(request.POST)
        except:
            form = forms.Signup()
        return HttpResponse(render(request,'form.html', {'form': form, 'form_id': a}))


def profile(request, pk):
    a = reverse('registration:profile', kwargs={'pk':pk})
    form = forms.Userinfo(request.POST)
    if form.is_valid():
        userinfo = form.save(commit=False)
        userinfo.user = User.objects.get(pk=pk)
        userinfo.save()
        return HttpResponseRedirect('/')
    else:
        try:
            form = forms.Userinfo(request.POST)
        except:
            form = forms.Userinfo()
        return HttpResponse(render(request,'form.html',{'form':form, 'form_id':a}))

def activate(request,uidb64,token):
    account_token = tokens.Activate_user()
    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)

    except:
        user = None

    if user is not None and account_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('successfully verified')
    else:
        return HttpResponse('invalid link')

@login_required()
def contact(request):
    form = forms.ContactForm()
    if request.method == "POST":
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['Subject']
            message = form.cleaned_data['Message']
            EmailMessage(subject,message,to=['iitbhuconnect@gmail.com']).send()
            return HttpResponseRedirect('/')
        else:
            return HttpResponse(render(request, 'registration/form.html', {'form': form}))
    else:
        return HttpResponse(render(request,'registration/form.html',{'form':form}))

@login_required()
def change_password(request):
    form = forms.Change_password(request.POST)
    if form.is_valid():
        if form.cleaned_data['new_password']!=form.cleaned_data['new_password1']:
            error = 'Passwords don`t match'
            return HttpResponse(render(request,'form_registered.html',{'form': form ,'error':error}))
        else:
            user = request.user
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            return HttpResponse(render(request, 'registration/change_password.html'))
    else:
        form = forms.Change_password()
        return HttpResponse(render(request, 'form_registered.html', {'form': form}))


class EditProfile(UpdateView):
    model = models.Userinfo
    fields = ['profile_picture', 'mobile_no', 'dob']
    ##success_url = '/welcome'

@login_required()
def edit(request):
    user = request.user
    try:
        pk = models.Userinfo.objects.get(user=user).pk
        return HttpResponseRedirect(reverse('registration:editprofile', kwargs={'pk':pk}))
    except:
        return  HttpResponseRedirect(reverse('registration:profile',kwargs={'pk':user.pk}))
def google(request):
    return  HttpResponse(render(request,'registration/google.html'))
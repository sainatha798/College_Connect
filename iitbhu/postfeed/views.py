from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from . import models
from . import forms
from django.forms import formset_factory
from django.urls import reverse
import datetime
# Create your views here.


@login_required()
def index(request):
    ##return HttpResponse(render(request ))
    return HttpResponse(render(request, 'postfeed/home.html'))
# Create your views here.

@login_required()
def feed(request):
    user = request.user
    query = models.Post.objects.filter(tag__userprefernces__user=user).distinct()
    return HttpResponse(render(request,'postfeed/post.html',{'query':query}))

class Add_post(CreateView):
    model = models.Post
    fields = ['text', 'pic', 'video', 'post_file', 'tag_no']


@login_required()
def addPostTag(request,pk):

    post = models.Post.objects.get(pk=pk)
    post.user = request.user
    post.save()
    n = post.tag_no
    if request.method == 'POST':
        formset = formset_factory(forms.AddPostTag)
        filled_forms = formset(request.POST)
        if filled_forms.is_valid():
            for form in filled_forms:
                try:
                    tag = models.Tag.objects.get(tag__iexact=form.cleaned_data['tag'])
                    tag.save()
                    tag.post.add(post)
                    tag.save()
                    continue
                except:
                    tag = models.Tag()
                    tag.tag  = form.cleaned_data['tag']
                    tag.save()
                    tag.post.add(post)
                    tag.save()
            return HttpResponseRedirect(reverse('postfeed:post_home'))
        else:
            tags = formset_factory(request.POST)
            error = 'invalid entries'
            return HttpResponse(render(request, 'postfeed/posttag_form.html', {'tags': tags, 'error':error}))

    else:
        tags = formset_factory(forms.AddPostTag , extra=n)
        return HttpResponse(render(request,'postfeed/posttag_form.html', {'tags':tags}))

@login_required()
def changepref(request):
    user = request.user
    try:
        qset = models.UserPrefernces.objects.get(user=user)
        queryset = qset.tags.all()
        c = 0
        if queryset.count() == 0:
            c=1

    except:
        qset = models.UserPrefernces()
        qset.user = user
        qset.save()
        queryset = qset.tags.all()
        c=1
    return HttpResponse(render(request, 'postfeed/changepref.html', {'set':queryset,'empty':c}))

def n(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('postfeed:addtag', kwargs={'n':request.POST['no_of_tags']}))
    else:
        form = forms.AddTagNo()
        return HttpResponse(render(request, 'postfeed/blankform.html', {'form':form}))
def addtag(request, n):
    user = models.UserPrefernces.objects.get(user=request.user)

    if request.method == 'POST':
        formset = formset_factory(forms.AddTag)
        formset = formset_factory(forms.AddPostTag)
        filled_forms = formset(request.POST)
        if filled_forms.is_valid():
            for form in filled_forms:
                try:
                    tag = models.Tag.objects.get(tag__iexact=form.cleaned_data['tag'])
                    user.tags.add(tag)
                    user.save()
                    continue
                except:
                    tag = models.Tag()
                    tag.tag = form.cleaned_data['tag']
                    tag.save()
                    user.tags.add(tag)
                    user.save()
            return HttpResponseRedirect(reverse('postfeed:changepref'))
        else:
            tags = formset_factory(request.POST)
            error = 'invalid entries'
            return HttpResponse(render(request, 'postfeed/posttag_form.html', {'tags': tags, 'error': error}))
    else:
        tags = formset_factory(forms.AddTag, extra=int(n))
        return HttpResponse(render(request, 'postfeed/posttag_form.html', {'tags': tags}))

def edit(request):
    user = request.user
    if request.method == 'POST':

        tag = request.POST.getlist('tags')

        for x in tag:

            a = models.UserPrefernces.objects.get(user=user)
            b = models.Tag.objects.get(tag=x)
            a.tags.remove(b)
            a.save()
        return HttpResponseRedirect(reverse('postfeed:changepref'))

    else:
        form = forms.Edit(request.user)
        error = 'Selected tags will be removed from preferences'
        return HttpResponse(render(request,'postfeed/blankform.html', {'form':form, 'error':error}))

@login_required()
def post(request):
    user = request.user
    query = models.Post.objects.filter(user=user)
    return HttpResponse(render(request,'postfeed/post.html',{'query':query}))

@login_required()
def rss(request):
	return HttpResponse(render(request,'postfeed/rss.html'))





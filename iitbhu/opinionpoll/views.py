from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import PollQuestion, PollChoice
from . import forms, models
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required()
def index(request):

    return HttpResponse(render(request,'opinionpoll/index.html'))
@login_required()
def polls(request):
    a = PollQuestion.objects.all()
    return HttpResponse(render(request, 'opinionpoll/viewpoll.html', {'ques': a,'c':1}))
@login_required()
def view_post(request, post_id):
    choice = PollQuestion.objects.get(pk=post_id).pollchoice_set.all()

    return HttpResponse(render(request,'opinionpoll/posts.html', {'choice': choice}))
@login_required()
def vote(request):
    a = PollQuestion.objects.all()
    return HttpResponse(render(request, 'opinionpoll/viewpoll.html', {'ques': a}))
@login_required()
def submit(request, vote_id):
    user = request.user
    x = models.PollQuestion.objects.get(pk=vote_id)
    if user not in x.voted.all():
        try:
            if request.POST['choices'] != 0:
                a = PollChoice.objects.get(id=request.POST['choices'])
                a.poll_count += 1
                a.save()
                x.voted.add(user)
                return HttpResponseRedirect(reverse('index'))
        except:
            form = forms.Vote(vote_id)
            return HttpResponse(render(request,'opinionpoll/submit.html',{'form': form, 'vote_id':vote_id}))
    else:
            return HttpResponse(render(request,'opinionpoll/error.html'))
@login_required()
def polled(request):
    a = PollChoice.objects.get(pk=int(request.POST['choices']))
    a.poll_count += 1
    a.save()
    return HttpResponse('good')
##@login_required()


class add_ques(CreateView):
    model = models.PollQuestion
    fields = ['poll_question','no_of_choices']


@login_required()
def add_choice(request,pk):
    user = request.user
    ques = PollQuestion.objects.get(id=pk)
    ques.user = user
    ques.save()
    n = ques.no_of_choices
    if request.method == 'POST':
        formset = formset_factory(forms.AddChoice)
        filled_forms = formset(request.POST)
        if filled_forms.is_valid():
            for form in filled_forms:
                a = form.save(commit=False)
                a.question = ques
                a.save()
            return HttpResponseRedirect(reverse('opinionpoll:polls'))
        else:
            return HttpResponse('sorry')
    else:
        choices = formset_factory(forms.AddChoice, extra=n)
        return HttpResponse(render(request,'opinionpoll/pollchoice_form.html',{'choices':choices, 'pk':pk}))
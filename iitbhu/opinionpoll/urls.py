__author__ = 'sainatha798'
from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'opinionpoll'

urlpatterns = [
    url(r'^$', views.index, name='poll_home'),
    url(r'^polls/$', views.polls, name='polls'),
    url(r'^(?P<post_id>[0-9]+)/',views.view_post, name='viewpost'),
    url(r'^vote/$', views.vote, name='vote'),
    url(r'^vote/(?P<vote_id>[0-9]+)/', views.submit, name='submit'),
    url(r'^submit/', views.polled, name='polled'),
    url(r'^add/ques/$', views.add_ques.as_view(), name='add_ques'),
    url(r'^add/ques/(?P<pk>[0-9]+)/', views.add_choice, name='add_choice'),

]

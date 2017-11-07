__author__ = 'sainatha798'
from django.conf.urls import url, include
from django.contrib import admin
from . import views
app_name = 'postfeed'
urlpatterns = [
    url(r'^$', views.index, name='post_home'),
    url(r'^post/$', views.Add_post.as_view(), name='addpost'),
    url(r'^postTag/(?P<pk>[0-9]+)/$', views.addPostTag, name='addPostTag'),
    url(r'^chgpref',views.changepref, name='changepref'),
    url(r'^addtag/$', views.n, name='n'),
    url(r'^addtag/(?P<n>[0-9]+)/$', views.addtag, name='addtag'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^user/$', views.post, name='user'),
    url(r'^feed/$', views.feed, name= 'feed'),
	url(r'^news_feed/$', views.rss, name= 'news_feed'),
]
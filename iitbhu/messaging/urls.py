from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'messaging'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^inbox/$', views.inbox, name='inbox'),
    url(r'^msg/(?P<pk>[0-9]+)$', views.mail, name='msg'),
    url(r'^outbox/$',views.outbox, name='outbox'),
    url(r'^trash/$', views.trash, name='trash'),
    url(r'^compose', views.Compose.as_view(), name='compose'),
    url(r'^encrypt/(?P<pk>[0-9]+)$', views.encrypt , name='encrypt'),
    url(r'^del/(?P<pk>[0-9]+)$', views.delete, name='delete'),
    url(r'^undo/(?P<pk>[0-9]+)/$', views.undo, name='undo')
]
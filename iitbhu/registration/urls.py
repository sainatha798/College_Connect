__author__ = 'sainatha798'
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.conf.urls.i18n import i18n_patterns

app_name = 'registration'

urlpatterns = [

    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^login$',views.login_view, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^signup/(?P<pk>[0-9]+)/$', views.profile, name='profile'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^changepassword/$', views.change_password, name='changepassword'),
    url(r'^edit/$', views.edit , name='edit'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.EditProfile.as_view(), name='editprofile'),
    url(r'^google/$', views.google,)
    ]
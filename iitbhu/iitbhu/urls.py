"""iitbhu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.conf.urls.i18n import i18n_patterns


urlpatterns = i18n_patterns(
    url(r'^$', views.welcome),
    url(r'^welcome',views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^postfeed/', include('postfeed.urls'), name='post'),
    url(r'^poll/', include('opinionpoll.urls'), name='poll'),

    url(r'^credits/$', views.credits, name='credits'),
    url(r'^mail/',include('messaging.urls'), name='msg'),

    url(r'^test/$',views.test, name='test'),
)

urlpatterns += [
     url('^social/', include('social_django.urls', namespace='social')),
     url(r'^register/', include('registration.urls'), name='register'),
 ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# -*- coding: utf-8 -*-

"""quizy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

import time

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.shortcuts import render

from rest_framework.routers import DefaultRouter

from quizy.views import (PageViewSet, user_data,
    MyLessonsViewSet, answers,
    lessons, new_page, lesson_archive, enroll_user,
    lesson_picture_upload, picture_picture_upload)
# LessonsViewSet,


def app(request):
    """
    Одностраничное приложение на JavaScript
    Исходный код: /app
    Настройки: /package.json
    """
    return render(request, 'app.html', {'django': settings, 'time': int(time.time())})

router = DefaultRouter()
router.register('pages', PageViewSet)
# router.register('lessons', LessonsViewSet)
router.register('mylessons', MyLessonsViewSet)
# router.register(r'lessons/(:?P<id>\d+)', LessonsViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^quizy/', include('quizy.urls')),

    url(r'^api/', include(router.urls), name='api'),
    url(r'^api/user', user_data, name='user'),
    url(r'^api/enroll_user/(\d+)?/?$', enroll_user, name='enroll_user'),
    url(r'^api/answers/(\d+)/$', answers, name='answers'),
    # url(r'^api/lessons/$', get_lessons, name='get_lessons'),
    url(r'^api/lessons/(\d+)?/?$', lessons, name='get_lessons'),
    url(r'^api/lessons/(\d+)/new_page/$', new_page, name='new_page'),
    url(r'^api/lessons/(\d+)/upload/$', lesson_picture_upload, name='lesson_picture_upload'),
    url(r'^api/pages/(\d+)/upload/$', picture_picture_upload, name='picture_picture_upload'),
    url(r'^api/archive/(\d+)?/?$', lesson_archive, name='lesson_archive'),

    # Авторизация
    url(r'^accounts/', include('users.urls')),


    # JS-приложение
    url(r'^$', app, name='app'),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [url(r'^.*$', app)]


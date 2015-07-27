# -*- coding: utf-8 -*-


import time

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.shortcuts import render

from rest_framework.routers import DefaultRouter

from quizy.views import (user_data,
    answers, play, get_mypupil, create_pupil,
    mylessons, demo_play, pupils,
    new_page, lesson_archive, enroll_pupil, enroll_course_pupil,
    reject_lesson, lesson_picture_upload, page_picture_upload)

from quizy.page import PageViewSet
from quizy.materials import courses, lessons
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
# router.register('mylessons', MyLessonsViewSet)
# router.register(r'lessons/(:?P<id>\d+)', LessonsViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^quizy/', include('quizy.urls')),

    url(r'^api/', include(router.urls), name='api'),
    url(r'^api/user', user_data, name='user'),
    url(r'^api/pupils', pupils, name='pupils'),
    url(r'^api/answers/(\d+)/$', answers, name='answers'),
    url(r'^api/get_mypupil/$', get_mypupil, name='get_mypupil'),
    url(r'^api/create_pupil/$', create_pupil, name='create_pupil'),
    url(r'^api/enroll_pupil/(\d+)?/?$', enroll_pupil, name='enroll_pupil'),
    url(r'^api/enroll_course_pupil/(\d+)?/?$', enroll_course_pupil, name='enroll_course_pupil'),


    # url(r'^api/lessons/$', get_lessons, name='get_lessons'),
    url(r'^api/play/(\d+)?/?$', play, name='run_play'),
    url(r'^api/demo/play/(\d+)?/?$', demo_play, name='run_demo_play'),
    url(r'^api/courses/(\d+)?/?$', courses, name='get_courses'),
    url(r'^api/lessons/(\d+)?/?$', lessons, name='get_lessons'),
    url(r'^api/lessons/(\d+)/new_page/$', new_page, name='new_page'),
    url(r'^api/lessons/(\d+)/upload/$', lesson_picture_upload, name='lesson_picture_upload'),
    url(r'^api/reject_lesson(\d+)/$', reject_lesson, name='reject_lesson'),
    url(r'^api/mylessons/$', mylessons, name='mylessons'),

    url(r'^api/pages/(\d+)/upload/$', page_picture_upload, name='page_picture_upload'),
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


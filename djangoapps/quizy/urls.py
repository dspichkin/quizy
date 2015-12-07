# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.conf.urls import patterns, include

from rest_framework.routers import DefaultRouter

from quizy.teacher import (enroll_teacher, demo_play, pupils, lesson_picture_upload, enroll)
from quizy.pupil import (mylessons, answers, play, reject_lesson, mystatistic, enroll_pupil)

from quizy.materials import courses, lessons
# from quizy.views import HomePageView

from quizy.page import PageViewSet
from quizy.views import (
    get_mypupil, create_pupil,
    statistic,
    new_page, enroll_course_pupil,
    get_last_lessons,
    page_picture_upload, get_tags,
    get_avatar)

from quizy.pupil import (public_play, start_lessons, upload_avatar, save_answers)

router = DefaultRouter()
router.register('pages', PageViewSet)

urlpatterns = patterns(
    '',
    # url(r'^$', HomePageView.as_view(), name="home"),
    url(r'^api/', include(router.urls), name='api'),

    url(r'^api/pupils', pupils, name='pupils'),
    url(r'^api/uploadavatar/?$', upload_avatar, name='upload_avatar'),
    url(r'^api/answers/(\d+)/$', answers, name='answers'),
    url(r'^api/get_mypupil/$', get_mypupil, name='get_mypupil'),
    url(r'^api/get_avatar/$', get_avatar, name='get_avatar'),
    url(r'^api/create_pupil/$', create_pupil, name='create_pupil'),
    url(r'^api/enroll/(\d+)?/?$', enroll, name='enroll'),
    url(r'^api/enroll_teacher/(\d+)?/?$', enroll_teacher, name='enroll_teacher'),
    url(r'^api/enroll_pupil/(\d+)?/?$', enroll_pupil, name='enroll_pupil'),
    url(r'^api/enroll_course_pupil/(\d+)?/?$', enroll_course_pupil, name='enroll_course_pupil'),


    url(r'^api/play/(\d+)?/?$', play, name='run_play'),
    url(r'^api/demo/play/(\d+)?/?$', demo_play, name='run_demo_play'),
    url(r'^api/public/play/(\d+)?/?$', public_play, name='run_public_play'),

    url(r'^api/courses/(\d+)?/?$', courses, name='get_courses'),
    url(r'^api/lessons/(\d+)?/?$', lessons, name='get_lessons'),
    url(r'^api/tags/?$', get_tags, name='get_tags'),
    url(r'^api/last_lessons/(\w+)?/?$', get_last_lessons, name='get_last_lessons'),
    url(r'^api/start_lessons/(\d+)/?$', start_lessons, name='start_lessons'),
    url(r'^api/lessons/(\d+)/new_page/$', new_page, name='new_page'),
    url(r'^api/lessons/(\d+)/upload/$', lesson_picture_upload, name='lesson_picture_upload'),
    url(r'^api/reject_lesson/(\d+)/$', reject_lesson, name='reject_lesson'),
    url(r'^api/mylessons/$', mylessons, name='mylessons'),
    url(r'^api/mystatistic/$', mystatistic, name='mystatistic'),
    url(r'^api/statistic/(\d+)?/?$', statistic, name='statistic'),

    url(r'^api/pages/(\d+)/upload/$', page_picture_upload, name='page_picture_upload'),

    url(r'^api/save_answers/(\d+)/$', save_answers, name='save_answers'),

)

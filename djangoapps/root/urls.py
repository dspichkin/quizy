# -*- coding: utf-8 -*-


import time

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.shortcuts import render
from django.views.i18n import javascript_catalog

from quizy.views import (user_data)


js_info_dict = {
    'packages': ('your.app.package',),
}


def app(request):
    """
    Одностраничное приложение на JavaScript
    Исходный код: /app
    Настройки: /package.json
    """
    return render(request, 'app.html', {'django': settings, 'time': int(time.time())})


# router.register('lessons', LessonsViewSet)
# router.register('mylessons', MyLessonsViewSet)
# router.register(r'lessons/(:?P<id>\d+)', LessonsViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^i18n/', include('i18n.urls')),
    url(r'^jsi18n/', javascript_catalog, js_info_dict),

    url(r'^', include('quizy.urls')),

    url(r'^api/user', user_data, name='user'),

    # Авторизация
    url(r'^accounts/', include('users.urls')),

    # JS-приложение
    url(r'^$', app, name='app'),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [url(r'^.*$', app)]



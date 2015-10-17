# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LMSConfig(AppConfig):
    name = 'quizy'
    verbose_name = _(u'СДО')

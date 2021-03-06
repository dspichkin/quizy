# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from HTMLParser import HTMLParser

# from django.utils.encoding import force_unicode
from django.core.mail import send_mail as sm
from django.core.mail import EmailMultiAlternatives


from rest_framework import serializers
# from django.conf import settings


def send_mail(email_topic, email_msg, email_from, email_to, fail_silently=False, html_content=""):
    # if settings.COLGATE_MAIL:
    if html_content:
        subject, from_email, to = email_topic, email_from, email_to
        text_content = email_msg
        html_content = html_content
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    else:
        sm(email_topic, email_msg, email_from,
            email_to, fail_silently)
    """
    else:
        if settings.DEBUG:
            print "-------------------------"
            print "       SEND MESSAGE"
            print "-------------------------"
            print "\nemail_from: %s\n" % force_unicode(email_from)
            print "email_to: %s" % force_unicode(email_to)
            print "\n\nemail_topic: %s" % force_unicode(email_topic)
            print "\nemail_msg:\n%s" % force_unicode(email_msg)
            print "\n--------------------------"
        else:
            print "Send email to %s" % force_unicode(email_to)
    """


class MLStripper(HTMLParser):
    start_custom = None
    end_custom = None

    def __init__(self):
        self.reset()
        self.fed = []
        self.containstags = False

    def handle_starttag(self, tag, attrs):
        self.containstags = False
        if tag.lower() == 'b':
            self.start_custom = '<b>'
            self.end_custom = '</b>'
        if tag.lower() == 'i':
            self.start_custom = '<i>'
            self.end_custom = '</i>'
        if tag.lower() == 's':
            self.start_custom = '<s>'
            self.end_custom = '</s>'
        if tag.lower() == 'p':
            self.start_custom = '<p>'
            self.end_custom = '</p>'
        if tag.lower() == 'br':
            self.start_custom = '<br>'
            self.end_custom = ''

    def handle_data(self, d):
        if self.start_custom:
            self.fed.append(self.start_custom + d + self.end_custom)
            self.start_custom = None
            self.end_custom = None
        else:
            self.fed.append(d)

    def has_tags(self):
        return self.containstags

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    must_filtered = True
    while must_filtered:
        s = MLStripper()
        s.feed(html)
        html = s.get_data()
        must_filtered = s.has_tags()
    return html


def normalize(data):
    """
    удаляем лишние теги из структуры урока 1
    {
      "active": true,
      "steps": []
    }
    """
    clean_data = {}
    if 'active' in data:
        clean_data['active'] = data['active']
    if 'steps' in data:
        steps = data.get("steps")
        clean_steps = []
        for step in steps:
            clean_step = {}
            clean_step['text'] = strip_tags(step['text'])
            clean_step['type'] = step['type']
            clean_step['number'] = step['number']
            clean_step['mode'] = step['mode']
            clean_steps.append(clean_step)
        clean_data['steps'] = clean_steps
    return clean_data


class JSONField(serializers.Field):
    """
    Сериализация JSON-полей
    """
    def __init__(self, default=None, **kwargs):
        super(JSONField, self).__init__(**kwargs)
        self.default = default

    def to_representation(self, obj):
        if isinstance(obj, basestring):
            try:
                return json.loads(obj)
            except ValueError:
                return json.loads(self.default)
        return obj

    def to_internal_value(self, data):
        return json.dumps(data, ensure_ascii=False)


def is_enrolls_different(old_dict, new_dict):
    """
    Сравнение двух назанчений
    """
    if old_dict is None or new_dict is None:
        return False

    new_steps = new_dict.get('steps', [])
    old_steps = old_dict.get('steps', [])
    if len(new_steps) > 0 and len(old_steps) > 0:
        last_new_step = new_steps[len(new_steps) - 1]
        last_old_step = old_steps[len(old_steps) - 1]
        # если кол-во шагов совпадает и последний шаг завершен
        if len(new_steps) == len(old_steps):
            if last_new_step.get('mode') != last_old_step.get('mode') and last_new_step.get('mode') == 'finish':
                return True

    return False

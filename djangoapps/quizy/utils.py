# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from HTMLParser import HTMLParser

# from django.utils.encoding import force_unicode
from django.core.mail import send_mail as sm
from django.core.mail import EmailMultiAlternatives
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
            clean_steps.append(clean_step)
        clean_data['steps'] = clean_steps
    return clean_data
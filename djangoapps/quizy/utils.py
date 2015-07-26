# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.encoding import force_unicode
from django.core.mail import send_mail as sm
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_mail(email_topic, email_msg, email_from, email_to, fail_silently=False, html_content=""):
    #if settings.COLGATE_MAIL:
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
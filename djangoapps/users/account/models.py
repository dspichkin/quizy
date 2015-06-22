# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
import os

from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.crypto import get_random_string
from django.contrib.auth.models import (AbstractUser, BaseUserManager)

from ..utils import build_absolute_uri
# from .. import app_settings as users_app_settings
from . import app_settings
from . import signals

# from .utils import user_email
from .managers import EmailConfirmationManager
from .adapter import get_adapter

from easy_thumbnails.files import get_thumbnailer

# from lms.models import Course, CourseEnroll


from .. import app_settings as allauth_app_settings


@python_2_unicode_compatible
class EmailConfirmation(models.Model):
    user = models.ForeignKey(allauth_app_settings.USER_MODEL,
                             verbose_name=_('user'))
    created = models.DateTimeField(verbose_name=_('created'),
                                   default=timezone.now)
    sent = models.DateTimeField(verbose_name=_('sent'), null=True)
    key = models.CharField(verbose_name=_('key'), max_length=64, unique=True)

    objects = EmailConfirmationManager()

    class Meta:
        verbose_name = _("email confirmation")
        verbose_name_plural = _("email confirmations")

    def __str__(self):
        return "confirmation for %s" % self.user.email

    @classmethod
    def create(cls, user):
        key = get_random_string(64).lower()
        return cls._default_manager.create(user=user,
                                           key=key)

    def key_expired(self):
        expiration_date = self.sent \
            + datetime.timedelta(days=app_settings
                                 .EMAIL_CONFIRMATION_EXPIRE_DAYS)
        return expiration_date <= timezone.now()
    key_expired.boolean = True

    def confirm(self, request):
        if not self.key_expired() and not self.user.verified:
            email_address = self.user.email
            get_adapter().confirm_email(request, self.user)
            signals.email_confirmed.send(sender=self.__class__,
                                         request=request,
                                         email_address=email_address)
            return email_address

    def send(self, request, signup=False, **kwargs):
        # current_site = kwargs["site"] if "site" in kwargs \
        #    else Site.objects.get_current()
        activate_url = reverse("account_confirm_email", args=[self.key])
        activate_url = build_absolute_uri(request,
                                          activate_url,
                                          protocol=app_settings.DEFAULT_HTTP_PROTOCOL)
        ctx = {
            "user": self.user,
            "activate_url": activate_url,
            # "current_site": current_site,
            "key": self.key,
        }
        if signup:
            email_template = 'account/email/email_confirmation_signup'
        else:
            email_template = 'account/email/email_confirmation'
        get_adapter().send_mail(email_template,
                                self.user.email,
                                ctx)
        self.sent = timezone.now()
        self.save()
        signals.email_confirmation_sent.send(sender=self.__class__,
                                             confirmation=self)

    def send_confirmation(self, request, signup=False):
        self.send(request, signup=signup)
        return self


class AccountManager(BaseUserManager):
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            email = username
        email = self.normalize_email(email)
        if not username:
            if email:
                username = email
            else:
                raise ValueError('The given username or email must be set')
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.update({'role': 'admin'})
        superuser = self._create_user(username, email, password, True, True,
                                      **extra_fields)
        return superuser


class Organization(models.Model):
    name = models.CharField('название', max_length=100)
    slug = models.SlugField('код для URL')

    def __unicode__(self):
        return self.name

    # def pay_for(self, course, until):
    #     """Оплачивает курс до заданной даты и обновляет дату оплаты в индивидуальных назначениях"""
    #     accounts = self.accounts.all()
    #     CourseEnroll.objects.filter(
    #         models.Q(learner__in=accounts) &
    #         models.Q(paid_until__isnull=True) | models.Q(paid_until__lt=until)
    #     ).update(paid_until=until)


def avatar_uploader(obj, fn):
    name, ext = os.path.splitext(fn)
    return os.path.join('avatars', obj.username + ext)

AbstractUser._meta.get_field('email')._unique = True
AbstractUser._meta.get_field('email').blank = False
AbstractUser._meta.get_field('email').null = False


class Account(AbstractUser):
    middle_name = models.CharField('отчество', max_length=50, blank=True)
    avatar = models.ImageField('аватар', upload_to=avatar_uploader, max_length=1024, blank=True)

    is_org = models.BooleanField('является ли администратором?', default=False)
    org = models.ForeignKey(Organization, verbose_name='администрирует организацию',
                            null=True, blank=True, related_name='admin', related_query_name='account')

    member_of = models.ManyToManyField(Organization, verbose_name='к каким организациям относится',
                                       blank=True, related_name='accounts',
                                       related_query_name='account')

    verified = models.BooleanField(verbose_name=_('verified'), default=False)

    number_of_pupil = models.IntegerField('кол-во учеников', default=0)

    objects = AccountManager()

    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super(Account, self).save(*args, **kwargs)

        # Создадим объекты назначений
        # enrolls = [CourseEnroll(learner=self, course=course)
        #     for course in Course.objects.exclude(enroll__learner__pk=self.pk)]
        # if enrolls:
        #    CourseEnroll.objects.bulk_create(enrolls)

        # Пропишем организацию
        if self.is_org:
            if self.org is None:
                try:
                    org = Organization.objects.get(slug=self.username)
                except Organization.DoesNotExist:
                    org = Organization(slug=self.username)
            else:
                org = self.org
            org.name = self.fio()
            org.save()
            self.org = org
            super(Account, self).save(update_fields=['org'])
            self.member_of.add(org)

    def fio(self):
        if self.first_name and self.last_name:
            if self.middle_name:
                return '%s %s %s' % (self.last_name, self.first_name, self.middle_name)
            return '%s %s' % (self.last_name, self.first_name)
        elif self.first_name or self.last_name:
            return self.first_name or self.last_name
        return self.username or self.email

    # def pay_for(self, course, until):
        # this_enroll = CourseEnroll.objects.get(course=course, learner=self)
        # this_enroll.paid_until = until
        # this_enroll.save(update_fields=['paid_until'])

    @property
    def role(self):
        return 'trainer' if self.is_org else 'learner'

    @property
    def thumbnail(self):
        options = {'size': (24, 24), 'crop': True}
        try:
            thumb = get_thumbnailer(self.avatar).get_thumbnail(options)
        except Exception as ex:
            # raise
            # TODO log or something
            thumb = None
        return thumb

    def get_avatar_url(self):
        thumb = self.thumbnail
        if thumb:
            return thumb.url
        return None


# Account._meta.get_field('email')._blank = False
# Account._meta.get_field('email')._null = False
# Account._meta.get_field('email')._unique = True


class User(Account):
    class Meta(Account.Meta):
        proxy = True


class InviteAlreadyUsed(Exception):
    pass

"""
class Invite(models.Model):
    owner = models.ForeignKey(Account, related_name='invites')
    # course = models.ForeignKey(Course, related_name='invites')
    user = models.ForeignKey(Account, null=True, blank=True, related_name='invite')

    #@classmethod
    #def create(cls, owner, course):
    #    cls._default_manager.create(owner=owner, course=course)

    #def invite_user(self, user):
    #    if self.user is not None:
    #        raise InviteAlreadyUsed(self.user)
    #    self.user = user
    #    dt = timezone.now()
    #    # На месяц вперед
    #    until = timezone.datetime(dt.year, dt.month % 12 + 1, * dt.timetuple()[2:7] + (dt.tzinfo,))
    #    user.pay_for(self.course, until)
    #    self.save()
    #    self.owner.org.accounts.add(user)

    class Meta:
        verbose_name = 'Инвайт'
        verbose_name_plural = 'Инвайты'

    def __unicode__(self):
        owner = self.owner and self.owner.username or '<пусто>'
        return '%s invite <id %s> (%s)' % (owner, self.pk or 'null', self.user or '<пусто>')

    def send_confirmation(self, request, user):
        confirmation = InviteConfirmation.create(self, user)
        confirmation.send(request)
        return confirmation


class InviteConfirmation(models.Model):
    user = models.ForeignKey(Account, verbose_name=_('user'))
    invite = models.ForeignKey(Invite)

    created = models.DateTimeField(verbose_name=_('created'),
                                   default=timezone.now)
    sent = models.DateTimeField(verbose_name=_('sent'), null=True)
    key = models.CharField(verbose_name=_('key'), max_length=64, unique=True)

    class Meta:
        verbose_name = 'Подтверждение инвайта'
        verbose_name_plural = 'Подтверждения инвайтов'

    def __unicode__(self):
        return 'confirmation for %s' % self.invite

    @classmethod
    def create(cls, invite, user):
        key = get_random_string(64).lower()
        return cls._default_manager.create(invite=invite, user=user, key=key)

    def key_expired(self):
        expiration_date = self.sent \
            + datetime.timedelta(days=app_settings
                                 .EMAIL_CONFIRMATION_EXPIRE_DAYS)
        return expiration_date <= timezone.now()
    key_expired.boolean = True

    def confirm(self, request):
        if not self.key_expired() and self.invite.user is None:
            self.invite.invite_user(self.user)
            signals.invite_confirmed.send(sender=self.__class__,
                                          request=request,
                                          email_address=email_address)
            return self.invite

    def send(self, request, **kwargs):
        # current_site = kwargs["site"] if "site" in kwargs \
        #    else get_current_site(request)
        activate_url = reverse("account_confirm_invite", args=[self.key])
        activate_url = build_absolute_uri(request,
                                          activate_url,
                                          protocol=app_settings.DEFAULT_HTTP_PROTOCOL)
        ctx = {
            "owner": self.invite.owner,
            "user": self.user,
            "activate_url": activate_url,
            # "current_site": current_site,
            "key": self.key,
        }

        email = EmailAddress.objects.get_primary(self.user).email
        template = 'account/email/invite_confirmation'
        get_adapter().send_mail(template, email, ctx, request)
        self.sent = timezone.now()
        self.save()
        signals.email_confirmation_sent.send(sender=self.__class__,
                                             confirmation=self)
"""


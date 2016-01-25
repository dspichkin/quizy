# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
import json
import shutil
import uuid

from random import randrange

from django.utils import timezone
from django.db import models, IntegrityError, transaction
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify as default_slugify

from sorl.thumbnail import ImageField

from json_field import JSONField

# from users.account.models import Account
try:
    from unidecode import unidecode
except ImportError:
    unidecode = lambda tag: tag

try:
    atomic = transaction.atomic
except AttributeError:
    from contextlib import contextmanager

    @contextmanager
    def atomic(using=None):
        sid = transaction.savepoint(using=using)
        try:
            yield
        except IntegrityError:
            transaction.savepoint_rollback(sid, using=using)
            raise
        else:
            transaction.savepoint_commit(sid, using=using)


class BaseModel(models.Model):
    uuid = models.UUIDField(max_length=36, unique=True, db_index=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name=u"Дата последнего обновления")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())

        super(BaseModel, self).save(*args, **kwargs)


def course_picture_upload(obj, fn):
    if not obj.uuid:
        obj.uuid = uuid.uuid4()
    fn, ext = os.path.splitext(fn)
    return os.path.join('courses', str(obj.uuid), '%s' % 'lesson_' + str(randrange(0, 9999)) + ext)


class Course(BaseModel):
    is_active = models.BooleanField(_(u'активен?'), default=True)
    name = models.CharField(_(u'название курса'), max_length=140, blank=True, null=True)
    description = models.TextField(_(u'описание'), blank=True)

    created_by = models.ForeignKey('account.Account', related_name='courses',
                                 verbose_name=_(u'создатель'), blank=True, null=True)

    teacher = models.ManyToManyField('account.Account', related_name='courses_teachers',
                                 verbose_name=_(u'преподователь'), blank=True, null=True)

    code_errors = JSONField(_(u'ошибки редактирования урока'), default={}, blank=True, null=True)
    is_correct = models.BooleanField(_(u'урок составлен верно?'), default=True)

    picture = ImageField(upload_to=course_picture_upload, blank=True, null=True)

    @property
    def type(self):
        return 'course'

    class Meta:
        verbose_name = _(u'Курс')
        verbose_name_plural = _(u'Курсы')
        app_label = 'quizy'

    def __unicode__(self):
        if self.name:
            return self.name
        return _(u"Курс без именени")

    @property
    def enroll_number(self):
        enrolls = {}
        for c in LessonEnroll.objects.filter(lesson__course=self):
            enrolls.update({
                c.pk: c
            })
        for c in self.course_enrolls.filter(course=self):
            enrolls.update({
                c.pk: c
            })
        return {
            'number': len(enrolls.keys())
        }

    def get_first_lesson(self):
        lessons = self.lesson_set.all().order_by('number')[:1]
        if lessons:
            return lessons[0]


def lesson_picture_upload(obj, fn):
    if not obj.uuid:
        obj.uuid = uuid.uuid4()
    fn, ext = os.path.splitext(fn)
    return os.path.join('lessons', str(obj.uuid)[:8], '%s' % 'lesson_' + str(randrange(0, 9999)) + ext)


class Lesson(BaseModel):

    def media_question_upload(obj, fn):
        if not obj.uuid:
            obj.uuid = uuid.uuid4()
        fn, ext = os.path.splitext(fn)
        return os.path.join('lessons', str(obj.uuid)[:8], 'media_%s%s' % (str(randrange(0, 9999)), ext))

    LESSON_TYPE_CHOICES = (
        ('inside', _(u'внутренний')),
        ('outside', _(u'внешний')),
    )

    LESSON_FULL_TYPE_CHOICES = (
        (1, _(u'внутренний урок')),
        (2, _(u'урок на написание писем')),
    )

    is_active = models.BooleanField(_(u'активен?'), default=True)
    is_public = models.BooleanField(_(u'опубликовать для всех'), default=False)
    name = models.CharField(_(u'название урока'), max_length=140, blank=True, null=True)
    number = models.IntegerField(_(u'порядок следования'), default=0)
    description = models.TextField(_(u'описание'), blank=True)
    created_by = models.ForeignKey('account.Account', related_name='lessons',
                                 verbose_name=_(u'создатель'), blank=True, null=True)
    teacher = models.ManyToManyField('account.Account', related_name='lessons_teachers',
                                 verbose_name=_(u'преподователь'), blank=True, null=True)

    course = models.ForeignKey('Course', verbose_name=_(u'курс'), blank=True, null=True)

    code_errors = JSONField(_(u'ошибки редактирования урока'), default={}, blank=True, null=True)
    is_correct = models.BooleanField(_(u'урок составлен верно?'), default=True)

    picture = ImageField(_(u'картинка урока'), upload_to=lesson_picture_upload, blank=True, null=True)

    lesson_type = models.CharField(_(u'тип урока'), max_length=10, default='inside', choices=LESSON_TYPE_CHOICES, blank=True, null=True)
    full_lesson_type = models.IntegerField(_(u'тип урока'), choices=LESSON_FULL_TYPE_CHOICES)

    path_content = models.CharField(_(u'путь к контенту'), max_length=255, blank=True, null=True)

    media = models.FileField(_(u'медиа урока'), upload_to=media_question_upload, blank=True, null=True)

    timer = models.IntegerField(_(u'таймер урока (сек)'), blank=True, null=True)

    tag = models.ManyToManyField('Tag', related_name='lessons_tags', verbose_name=_(u'метки'), blank=True, null=True)

    class Meta:
        ordering = ('number', )
        verbose_name = _(u'Урок')
        verbose_name_plural = _(u'Уроки')
        app_label = 'quizy'

    def __unicode__(self):
        if self.name:
            return self.name
        return _(u"Урок без именени")

    def save(self, *args, **kwargs):
        if self.full_lesson_type == 2:
            self.lesson_type = 'outside'
            self.path_content = '1'
        super(Lesson, self).save(*args, **kwargs)

    @property
    def content(self):
        if self.lesson_type != 'inside':
            path = os.path.join(settings.BASE_DIR, 'app', 'assets', 'lessons', self.path_content)
            json_path = os.path.join(path, 'index.json')
            data = json.load(open(json_path))
            return {
                'controller': data.get('controller'),
                'teacher_controller': data.get('teacher_controller'),
                'template': data.get('template'),
                'teacher_template': data.get('teacher_template'),
                'path': '/assets/lessons/%s/' % self.path_content
            }
        else:
            return {}

    def set_code_errors(self, code_errors):
        if self.lesson_type == 'inside':
            self.code_errors = code_errors
            self.save()


@receiver(pre_delete, sender=Lesson, dispatch_uid='lesson_delete_signal')
def pre_deleted_lesson(sender, instance, using, **kwargs):
    """
    удаления медиа вместе с уроком
    """
    directory = os.path.join(settings.MEDIA_ROOT, 'lessons', str(instance.uuid)[:8])
    if os.path.exists(directory):
        shutil.rmtree(directory)


class Tag(models.Model):
    name = models.CharField(verbose_name=_(u'Имя'), unique=True, max_length=100)
    slug = models.SlugField(verbose_name=_(u'Слаг'), unique=True, max_length=100)

    class Meta:
        verbose_name = _(u"Метка")
        verbose_name_plural = _(u"Метки")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = self.slugify(self.name)
            from django.db import router
            using = kwargs.get("using") or router.db_for_write(
                type(self), instance=self)
            # Make sure we write to the same db for all attempted writes,
            # with a multi-master setup, theoretically we could try to
            # write and rollback on different DBs
            kwargs["using"] = using
            # Be oportunistic and try to save the tag, this should work for
            # most cases ;)
            try:
                with atomic(using=using):
                    res = super(Tag, self).save(*args, **kwargs)
                return res
            except IntegrityError:
                pass
            # Now try to find existing slugs with similar names
            slugs = set(
                self.__class__._default_manager
                .filter(slug__startswith=self.slug)
                .values_list('slug', flat=True)
            )
            i = 1
            while True:
                slug = self.slugify(self.name, i)
                if slug not in slugs:
                    self.slug = slug
                    # We purposely ignore concurrecny issues here for now.
                    # (That is, till we found a nice solution...)
                    return super(Tag, self).save(*args, **kwargs)
                i += 1
        else:
            return super(Tag, self).save(*args, **kwargs)

    def slugify(self, tag, i=None):
        slug = default_slugify(unidecode(tag))
        if i is not None:
            slug += "_%d" % i
        return slug


class CourseEnroll(BaseModel):
    """
    Назначения на курсы индивидульных пользователей
    """
    learner = models.ForeignKey('account.Account', related_name='course_enrolls',
                                verbose_name=_(u'обучаемый'))
    created_by = models.ForeignKey('account.Account', related_name='course_enrolls_created',
                                verbose_name=_(u'кто создал назначение'))
    course = models.ForeignKey('Course', related_name='course_enrolls',
                            verbose_name=_(u'курс'), blank=True, null=True)

    auto_enroll = models.BooleanField(_(u'авто назначения на уроки'), default=False)

    data = JSONField(_(u'данные прохождения'), default={}, blank=True, null=True)
    last_data = models.DateTimeField(_(u'дата последней попытки'), null=True, blank=True)
    number_of_attempt = models.IntegerField(_(u'кол-во попыток'), default=0)
    success = models.NullBooleanField(_(u'результат последней попытки прохождения'), null=True, blank=True)
    is_archive = models.BooleanField(_(u'урок в архиве'), default=False)
    date_archive = models.DateTimeField(_(u'дата перемещения в архиве'), null=True, blank=True)
    #  TODO: собирать статистику по прохождению

    class Meta:
        verbose_name = _(u'Назначение на курс')
        verbose_name_plural = _(u'Назначения на курсы')
        app_label = 'quizy'

    def __unicode__(self):
        return '%s(%s)' % (self.learner, self.course.name.lower())

    @classmethod
    def create(cls, course, learner, created_by):
        enroll = cls.objects.create(course=course, learner=learner, created_by=created_by)
        first_lesson = enroll.course.get_first_lesson()
        if first_lesson:
            LessonEnroll.objects.get_or_create(lesson=first_lesson, learner=learner, created_by=created_by)
        return enroll


class LessonEnroll(BaseModel):
    """
    Назначения на курсы индивидульных пользователей
    """
    learner = models.ForeignKey('account.Account', related_name='lesson_enrolls',
                                verbose_name=_(u'обучаемый'))
    created_by = models.ForeignKey('account.Account', related_name='lesson_enrolls_created',
                                verbose_name=_(u'кто создал назначение'))
    teachers = models.ManyToManyField('account.Account', related_name='lesson_enrolls_teachers',
                                 verbose_name=_(u'преподователь'), blank=True, null=True)
    # course = models.ForeignKey('CourseEnroll', related_name='lesson_enrolls',
    #                        verbose_name='курс', blank=True, null=True)
    lesson = models.ForeignKey('Lesson', related_name='enrolls',
                            verbose_name=_(u'урок'), blank=True, null=True)

    data = JSONField(_(u'результат прохождения'), default={}, blank=True, null=True)
    # last_data = models.DateTimeField('дата последней попытки', null=True, blank=True)
    number_of_attempt = models.IntegerField(_(u'кол-во попыток'), default=0)
    success = models.NullBooleanField(_(u'результат последней попытки прохождения'), null=True, blank=True)
    date_success = models.DateTimeField(_(u'дата последней успешной попытки'), null=True, blank=True)
    #  TODO: собирать статистику по прохождению
    required_attention_by_teacher = models.NullBooleanField(_(u'требуется внимание со стороны преподователя'), null=True, blank=True)
    required_attention_by_pupil = models.NullBooleanField(_(u'требуется внимание со стороны студента'), null=True, blank=True)

    class Meta:
        verbose_name = _(u'Назначение на урок')
        verbose_name_plural = _(u'Назначения на уроки')
        app_label = 'quizy'

    def __unicode__(self):
        if self.lesson:
            return '%s (%s)' % (self.learner, self.lesson.name.lower())
        return '%s (назначение без урока)' % (self.learner)

    @property
    def is_locked(self):
        return not self.is_active
    is_locked.setter

    def is_locked(self, value):
        self.is_active = not value

    @property
    def has_permission(self):
        return self.is_active and bool(self.paid_until) and timezone.now() <= self.paid_until

"""
TASK_ERRORS = {
    '100': 'Нет ни одного вопроса',
}

QUESTION_ERRORS = {
    '100': 'Нет ни одного ответа',
    '101': 'Не выбран ни один правильный ответ',
    '102': 'В одном из ответов поле текст не заполнено',
    '103': 'Поле текст вопроса не заполнено',
    '104': 'В одной или несколько пар в правой части не заполнено поле текст',
    '105': 'Для данного типа вопроса коли-во ответов должно быть два и более'
}

ANSWER_ERRORS = {
    # '100': 'Поле текст ответа не заполнен',
}
"""


def media_question_upload(obj, fn):
    fn, ext = os.path.splitext(fn)
    return os.path.join('lessons', str(obj.lesson.uuid), 'question_%s%s' % (str(randrange(0, 9999)), ext))


class Page(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('radiobox', _(u'Вопрос с выбором одного ответа')),
        ('checkbox', _(u'Вопрос с выбором нескольких ответов')),
        ('text', _(u'Текстовый вопрос')),
        ('pairs', _(u'Вопрос с подбором пары')),
        ('words_in_text', _(u'Страница с подбором слов в тексте'))
    )

    lesson = models.ForeignKey('Lesson', related_name='pages',
                            related_query_name='page',
                            verbose_name=_(u'курс'), editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    type = models.CharField(
        _(u'тип вопроса'), max_length=10, default='radio',
        choices=QUESTION_TYPE_CHOICES)

    text = models.TextField(_(u'Вопрос'), blank=True, null=True)
    number = models.IntegerField(_(u'Порядок'), default=1, blank=True, null=True)

    media = models.FileField(upload_to=media_question_upload, blank=True, null=True)

    is_correct = models.BooleanField(_(u'правильность заполнения вопроса'), default=True)
    code_errors = JSONField(_(u'коды ошибок'), default={}, blank=True, null=True)

    def __unicode__(self):
        if self.text:
            return self.text
        return u"Вопрос с id %s" % self.id

    class Meta:
        verbose_name = _(u'Страница')
        verbose_name_plural = _(u'Страницы')
        ordering = ('number', 'created_at', 'text',)


class Variant(models.Model):
    PAIR_TYPE_CHOICES = (
        ('question', _(u'вопрос')),
        ('answer', _(u'ответ'))
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    text = models.TextField(_(u'текст ответа'), null=True, blank=True)
    pair = models.ForeignKey('self', null=True, blank=True, verbose_name=_(u'пара'))
    pair_type = models.CharField(_(u'тип пары'), max_length=10, default='question', choices=PAIR_TYPE_CHOICES)

    right_answer = models.BooleanField(default=False)

    page = models.ForeignKey(Page, related_name="variants")
    number = models.IntegerField(_(u'Порядок'), default=1)

    is_correct = models.BooleanField(_(u'правильность заполнения вопроса'), default=True)
    code_errors = JSONField(_(u'коды ошибок'), default={}, blank=True, null=True)
    reflexy = models.TextField(_(u'текст рефлексии'), null=True, blank=True)

    def __unicode__(self):
        if self.text:
            return self.text
        return u"Ответ на вопрос с id %s" % self.id

    class Meta:
        verbose_name = _(u'Ответ')
        verbose_name_plural = _(u'Ответы')
        ordering = ('number', 'created_at', 'text', )

    # def save(self, *args, **kwargs):
    #    super(Variant, self).save(*args, **kwargs)


class Statistic(models.Model):
    REASON_CHOICES = (
        ('success', _(u'Успешно выполено')),
        ('reject', _(u'Отказался выполнять')),
        ('done_time', _(u'Время вышло')),
        ('not_done', _(u'Не приступал')),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    lesson = models.ForeignKey('Lesson', related_name='statistics',
                            verbose_name=_(u'урок'), blank=True, null=True, on_delete=models.SET_NULL)
    learner = models.ForeignKey('account.Account', related_name='statistics',
                                verbose_name=_(u'обучаемый'), blank=True, null=True, on_delete=models.SET_NULL)
    number_of_attempt = models.IntegerField(_(u'кол-во попыток'), default=0)
    success = models.NullBooleanField(_(u'результат последней попытки прохождения'), null=True, blank=True)
    reason = models.CharField(_(u'причина перемещеня в статистику'), max_length=10, choices=REASON_CHOICES, null=True, blank=True)
    data = JSONField(_(u'данные прохождения'), default={}, blank=True, null=True)

    class Meta:
        verbose_name = _(u'Статистика/Архив')
        verbose_name_plural = _(u'Статистика/Архив')
        ordering = ('-updated_at', '-created_at', )

    



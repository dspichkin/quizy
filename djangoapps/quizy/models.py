# -*- coding: utf-8 -*-
import os

from uuid import uuid1
from random import randrange

from django.utils import timezone
from django.db import models

from sorl.thumbnail import ImageField

from json_field import JSONField

# from users.account.models import Account


class BaseModel(models.Model):
    uuid = models.CharField(max_length=36, unique=True, db_index=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.id or not self.uuid:
            u = uuid1()
            self.uuid = str(u)

        super(BaseModel, self).save(*args, **kwargs)


class Course(BaseModel):
    is_active = models.BooleanField('активен?', default=True)
    name = models.CharField('название курса', max_length=140, blank=True, null=True)
    description = models.TextField('описание', blank=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        app_label = 'quizy'

    def __unicode__(self):
        if self.name:
            return self.name
        return u"Курс без именени"


def picture_upload(obj, fn):
    if obj.pk:
        fn, ext = os.path.splitext(fn)
        return os.path.join('lessons', str(obj.pk), '%s' % 'lesson_' + str(randrange(0, 9999)) + ext)
    else:
        raise Exception("Сохраните урок до загрузки изображения")


class Lesson(BaseModel):

    is_active = models.BooleanField('активен?', default=True)

    name = models.CharField('название урока', max_length=140, blank=True, null=True)

    number = models.IntegerField('порядок следования', default=0)
    description = models.TextField('описание', blank=True)

    created_by = models.ForeignKey('account.Account', related_name='lessons',
                                 verbose_name='создатель', blank=True, null=True)

    course = models.ForeignKey('Course', verbose_name='курс', blank=True, null=True)

    code_errors = JSONField('ошибки редактирования урока', default={}, blank=True, null=True)
    is_correct = models.BooleanField('урок составлен верно?', default=True)

    picture = ImageField(upload_to=picture_upload, blank=True, null=True)

    class Meta:
        ordering = ('created_by', 'number')
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        app_label = 'quizy'

    def __unicode__(self):
        if self.name:
            return self.name
        return u"Урок без именени"


class LessonEnroll(BaseModel):
    """
    Назначения на курсы индивидульных пользователей
    """
    learner = models.ForeignKey('account.Account', related_name='enrolls',
                                verbose_name='обучаемый')
    created_by = models.ForeignKey('account.Account', related_name='enroll_created',
                                verbose_name='кто создал назначение')
    course = models.ForeignKey('Course', related_name='enrolls',
                            verbose_name='курс', blank=True, null=True)
    lesson = models.ForeignKey('Lesson', related_name='enrolls',
                            verbose_name='урок', blank=True, null=True)

    data = JSONField('результат прохождения', default={})
    last_data = models.DateTimeField('дата последней попытки', null=True, blank=True)
    number_of_attempt = models.IntegerField('кол-во попыток', default=0)
    success = models.NullBooleanField('результат последней попытки прохождения', null=True, blank=True)
    is_archive = models.BooleanField('урок в архиве', default=False)
    date_archive = models.DateTimeField('дата перемещения в архиве', null=True, blank=True)
    #  TODO: собирать статистику по прохождению

    class Meta:
        verbose_name = 'Назначение'
        verbose_name_plural = 'Назначения'
        app_label = 'quizy'

    def __unicode__(self):
        return '%s(%s)' % (self.learner, self.lesson.name.lower())

    @property
    def is_locked(self):
        return not self.is_active
    is_locked.setter

    def is_locked(self, value):
        self.is_active = not value

    @property
    def has_permission(self):
        return self.is_active and bool(self.paid_until) and timezone.now() <= self.paid_until


class Attempt(models.Model):
    enroll = models.ForeignKey(LessonEnroll, related_name='attempts',
                               related_query_name='attempt', default=0)

    is_best = models.BooleanField(default=False, editable=False)
    is_last = models.BooleanField(default=False, editable=False)

    points = models.IntegerField(default=0)
    num = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    duration = models.IntegerField(default=0)

    data = JSONField(default='{}')

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'

    def __unicode__(self):
        return '%s / %s Attempt #%d' % (self.lesson, self.learner, self.num)


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


def picture_question_upload(obj, fn):
    if obj.pk:
        fn, ext = os.path.splitext(fn)
        return os.path.join('lessons', str(obj.lesson.pk), 'question_%s%s' % (str(obj.id) + '_' + str(randrange(0, 9999)), ext))
    else:
        raise Exception("Сохраните вопрос до загрузки изображения")


class Page(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('radiobox', 'Вопрос с выбором одного ответа'),
        ('checkbox', 'Вопрос с выбором нескольких ответов'),
        ('text', 'Текстовый вопрос'),
        ('pairs', 'Вопрос с подбором пары')
    )

    lesson = models.ForeignKey('Lesson', related_name='pages',
                            related_query_name='page',
                            verbose_name='курс', editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    type = models.CharField(
        'тип вопроса', max_length=10, default='radio',
        choices=QUESTION_TYPE_CHOICES)

    text = models.TextField('Вопрос', blank=True, null=True)
    number = models.IntegerField('Порядок', default=1, blank=True, null=True)

    picture = ImageField(upload_to=picture_question_upload, blank=True, null=True)

    is_correct = models.BooleanField('правильность заполнения вопроса', default=True)
    code_errors = JSONField('коды ошибок', default={}, blank=True, null=True)

    def __str__(self):
        if self.text:
            return self.text
        return u"Вопрос с id %s" % self.id

    def __unicode__(self):
        if self.text:
            return self.text
        return u"Вопрос с id %s" % self.id

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
        ordering = ('number', 'created_at', 'text',)


class Variant(models.Model):
    PAIR_TYPE_CHOICES = (
        ('question', 'вопрос'),
        ('answer', 'ответ')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    text = models.TextField('текст ответа', null=True, blank=True)
    pair = models.ForeignKey('self', null=True, blank=True, verbose_name='пара')
    pair_type = models.CharField('тип пары', max_length=10, default='question', choices=PAIR_TYPE_CHOICES)

    right_answer = models.BooleanField(default=False)

    page = models.ForeignKey(Page, related_name="variants")
    number = models.IntegerField('Порядок', default=1)

    is_correct = models.BooleanField('правильность заполнения вопроса', default=True)
    code_errors = JSONField('коды ошибок', default={}, blank=True, null=True)

    def __str__(self):
        if self.text:
            return self.text
        return u"Ответ на вопрос с id %s" % self.id

    def __unicode__(self):
        if self.text:
            return self.text
        return u"Ответ на вопрос с id %s" % self.id

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ('number', 'created_at', 'text', )

    # def save(self, *args, **kwargs):
    #    super(Variant, self).save(*args, **kwargs)


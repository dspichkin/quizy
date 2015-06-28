# -*- coding: utf-8 -*-

from uuid import uuid1

from django.utils import timezone
from django.db import models

from json_field import JSONField

# from users.account.models import Account


class BaseModel(models.Model):
    uuid = models.CharField(max_length=36, unique=True, db_index=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.id or not self.uuid:
            u = uuid1()
            self.uuid = str(u)

        super(BaseModel, self).save(*args, **kwargs)


class LessonEnroll(models.Model):
    """
    Назначения на курсы индивидульных пользователей
    """
    created_at = models.DateTimeField('назначено', auto_now_add=True)
    updated_at = models.DateTimeField('последняя попытка', auto_now=True)
    learner = models.ForeignKey('account.Account', related_name='enrolls',
                                related_query_name='enroll',
                                verbose_name='обучаемый', editable=False)
    lesson = models.ForeignKey('Lesson', related_name='enrolls',
                            related_query_name='enroll',
                            verbose_name='курс', editable=False)
    is_active = models.BooleanField('урок доступен?', default=True)
    result = JSONField('результат прохождения', default='{}')
    number_of_attempt = models.IntegerField('кол-во попыток', default=0)
    success = models.NullBooleanField('результат последней попытки прохождения', null=True, blank=True)
    is_archive = models.BooleanField('урок в архиве', default=False)
    date_archive = models.DateTimeField('дата перемещения в архиве', null=True, blank=True)
    #  TODO: собирать статистику по прохождению

    class Meta:
        verbose_name = 'Назначение'
        verbose_name_plural = 'Назначения'

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


class Lesson(models.Model):

    is_active = models.BooleanField('активен?', default=True)

    name = models.CharField('название урока', max_length=140, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    number = models.IntegerField('порядок следования', default=0)
    description = models.TextField('описание', blank=True)

    created_by = models.ForeignKey('account.Account', related_name='lessons',
                                 related_query_name='lesson',
                                 verbose_name='создатель', blank=True, null=True)

    class Meta:
        ordering = ('created_by', 'number')
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __unicode__(self):
        if self.name:
            return self.name
        return u"Урок без именени"

    # def save(self, *args, **kwargs):
        # Создадим назначения по необходимости
        # enrolls = [LessonEnroll(learner=ac, lesson=self)
        #     for ac in Account.objects.exclude(enroll__lesson__pk=self.pk)]
        # if enrolls:
        #    LessonEnroll.objects.bulk_create(enrolls)

    # def url(self):
    #    return '/assets/lessons/%s/index.json' % self.path


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


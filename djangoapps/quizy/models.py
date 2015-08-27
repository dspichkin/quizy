# -*- coding: utf-8 -*-
import os
import json
import shutil

from uuid import uuid1
from random import randrange

from django.utils import timezone
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver

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


def course_picture_upload(obj, fn):
    if obj.pk:
        fn, ext = os.path.splitext(fn)
        return os.path.join('courses', str(obj.pk), '%s' % 'lesson_' + str(randrange(0, 9999)) + ext)
    else:
        raise Exception("Сохраните курс до загрузки изображения")


class Course(BaseModel):
    is_active = models.BooleanField('активен?', default=True)
    name = models.CharField('название курса', max_length=140, blank=True, null=True)
    description = models.TextField('описание', blank=True)

    created_by = models.ForeignKey('account.Account', related_name='courses',
                                 verbose_name='создатель', blank=True, null=True)

    teacher = models.ManyToManyField('account.Account', related_name='courses_teachers',
                                 verbose_name='преподователь', blank=True, null=True)

    code_errors = JSONField('ошибки редактирования урока', default={}, blank=True, null=True)
    is_correct = models.BooleanField('урок составлен верно?', default=True)

    picture = ImageField(upload_to=course_picture_upload, blank=True, null=True)

    @property
    def type(self):
        return 'course'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        app_label = 'quizy'

    def __unicode__(self):
        if self.name:
            return self.name
        return u"Курс без именени"

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
    if obj.pk:
        fn, ext = os.path.splitext(fn)
        return os.path.join('lessons', str(obj.pk), '%s' % 'lesson_' + str(randrange(0, 9999)) + ext)
    else:
        raise Exception("Сохраните урок до загрузки изображения")


class Lesson(BaseModel):
    def media_question_upload(obj, fn):
        if obj.pk:
            fn, ext = os.path.splitext(fn)
            return os.path.join('lessons', str(obj.pk), 'media_%s%s' % (str(obj.id) + '_' + str(randrange(0, 9999)), ext))
        else:
            raise Exception("Сохраните вопрос до загрузки изображения")

    LESSON_TYPE_CHOICES = (
        ('inside', 'внутренний'),
        ('outside', 'внешний'),
    )

    is_active = models.BooleanField('активен?', default=True)

    name = models.CharField('название урока', max_length=140, blank=True, null=True)

    number = models.IntegerField('порядок следования', default=0)
    description = models.TextField('описание', blank=True)

    created_by = models.ForeignKey('account.Account', related_name='lessons',
                                 verbose_name='создатель', blank=True, null=True)

    teacher = models.ManyToManyField('account.Account', related_name='lessons_teachers',
                                 verbose_name='преподователь', blank=True, null=True)

    course = models.ForeignKey('Course', verbose_name='курс', blank=True, null=True)

    code_errors = JSONField('ошибки редактирования урока', default={}, blank=True, null=True)
    is_correct = models.BooleanField('урок составлен верно?', default=True)

    picture = ImageField(upload_to=lesson_picture_upload, blank=True, null=True)

    lesson_type = models.CharField('тип урока', max_length=10, default='inside', choices=LESSON_TYPE_CHOICES)
    path_content = models.CharField('путь к контенту', max_length=255, blank=True, null=True)

    media = models.FileField('медиа урока', upload_to=media_question_upload, blank=True, null=True)

    timer = models.IntegerField('таймер урока (сек)', blank=True, null=True)

    class Meta:
        ordering = ('number', )
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        app_label = 'quizy'

    def __unicode__(self):
        if self.name:
            return self.name
        return u"Урок без именени"

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
    directory = os.path.join(settings.MEDIA_ROOT, 'lessons', str(instance.pk))
    if os.path.exists(directory):
        shutil.rmtree(directory)


class CourseEnroll(BaseModel):
    """
    Назначения на курсы индивидульных пользователей
    """
    learner = models.ForeignKey('account.Account', related_name='course_enrolls',
                                verbose_name='обучаемый')
    created_by = models.ForeignKey('account.Account', related_name='course_enrolls_created',
                                verbose_name='кто создал назначение')
    course = models.ForeignKey('Course', related_name='course_enrolls',
                            verbose_name='курс', blank=True, null=True)

    auto_enroll = models.BooleanField('авто назначения на уроки', default=False)

    data = JSONField('данные', default={}, blank=True, null=True)
    last_data = models.DateTimeField('дата последней попытки', null=True, blank=True)
    number_of_attempt = models.IntegerField('кол-во попыток', default=0)
    success = models.NullBooleanField('результат последней попытки прохождения', null=True, blank=True)
    is_archive = models.BooleanField('урок в архиве', default=False)
    date_archive = models.DateTimeField('дата перемещения в архиве', null=True, blank=True)
    #  TODO: собирать статистику по прохождению

    class Meta:
        verbose_name = 'Назначение на курс'
        verbose_name_plural = 'Назначения на курсы'
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
                                verbose_name='обучаемый')
    created_by = models.ForeignKey('account.Account', related_name='lesson_enrolls_created',
                                verbose_name='кто создал назначение')
    # course = models.ForeignKey('CourseEnroll', related_name='lesson_enrolls',
    #                        verbose_name='курс', blank=True, null=True)
    lesson = models.ForeignKey('Lesson', related_name='enrolls',
                            verbose_name='урок', blank=True, null=True)

    data = JSONField('результат прохождения', default={}, blank=True, null=True)
    # last_data = models.DateTimeField('дата последней попытки', null=True, blank=True)
    number_of_attempt = models.IntegerField('кол-во попыток', default=0)
    success = models.NullBooleanField('результат последней попытки прохождения', null=True, blank=True)
    date_success = models.DateTimeField('дата последней успешной попытки', null=True, blank=True)
    #  TODO: собирать статистику по прохождению
    required_attention_by_teacher = models.NullBooleanField('требуется внимание со стороны преподователя', null=True, blank=True)
    required_attention_by_pupil = models.NullBooleanField('требуется внимание со стороны студента', null=True, blank=True)

    class Meta:
        verbose_name = 'Назначение на урок'
        verbose_name_plural = 'Назначения на уроки'
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
class Attempt(models.Model):
    enroll = models.ForeignKey(LessonEnroll, related_name='attempts',
                               related_query_name='attempt', default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    data = JSONField(default='{}')

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'

    def __unicode__(self):
        return '%s / %s Attempt #%d' % (self.lesson, self.learner, self.num)
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


def media_question_upload(obj, fn):
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
        ('pairs', 'Вопрос с подбором пары'),
        ('words_in_text', 'Страница с подбором слов в тексте')
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

    media = models.FileField(upload_to=media_question_upload, blank=True, null=True)

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
    reflexy = models.TextField('текст рефлексии', null=True, blank=True)

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


class Statistic(models.Model):
    REASON_CHOICES = (
        ('success', 'Успешно выполено'),
        ('reject', 'Отказался выполнять'),
        ('done_time', 'Время вышло'),
        ('not_done', 'Не приступал'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    lesson = models.ForeignKey('Lesson', related_name='statistics',
                            verbose_name='урок', blank=True, null=True, on_delete=models.SET_NULL)
    learner = models.ForeignKey('account.Account', related_name='statistics',
                                verbose_name='обучаемый', blank=True, null=True, on_delete=models.SET_NULL)
    number_of_attempt = models.IntegerField('кол-во попыток', default=0)
    success = models.NullBooleanField('результат последней попытки прохождения', null=True, blank=True)
    reason = models.CharField('причина перемещеня в статистику', max_length=10, choices=REASON_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'

    



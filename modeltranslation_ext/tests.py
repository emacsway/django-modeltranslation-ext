from __future__ import absolute_import, unicode_literals
from django.conf import settings
from django.db import models
from django.test import TestCase
from django.test.utils import override_settings
from django.utils import translation

from modeltranslation import translator

from .managers import ml_manager


class TestModel(models.Model):
    untrans = models.CharField('untrans', max_length=255)
    trans = models.CharField('trans', max_length=255)
    objects = ml_manager(models.Manager)()


class TestTranslationOptions(translator.TranslationOptions):
    fields = ('trans',)

OLD_LANGUAGE_CODE = settings.LANGUAGE_CODE
OLD_LANGUAGES = settings.LANGUAGES
OLD_USE_I18N = settings.USE_I18N

settings.LANGUAGE_CODE = 'ru'
settings.LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)
settings.USE_I18N = True

translator.translator.register(TestModel, TestTranslationOptions)

settings.LANGUAGE_CODE = OLD_LANGUAGE_CODE
settings.LANGUAGES = OLD_LANGUAGES
settings.USE_I18N = OLD_USE_I18N


@override_settings(
    LANGUAGE_CODE='ru',
    LANGUAGES=(
        ('ru', 'Russian'),
        ('en', 'English'),
    ),
    USE_I18N=True
)
class ModeltranslationExtTest(TestCase):

    def setUp(self):
        self.data = [
            {'id': 1,
             'untrans': 'untrans1',
             'trans': 'trans1',
             'trans_ru': 'trans1-ru',
             'trans_en': 'trans1-en', },
            {'id': 2,
             'untrans': 'untrans2',
             'trans': 'trans2',
             'trans_ru': 'trans2-ru',
             'trans_en': 'trans2-en', },
            {'id': 3,
             'untrans': 'untrans3',
             'trans': 'trans3',
             'trans_ru': 'trans3-ru',
             'trans_en': 'trans3-en', },
        ]
        for row in self.data:
            TestModel.objects.create(**row)

        self.old_data = {
            'CURRENT_LANGUAGE': translation.get_language()
        }

    def test_manager(self):
        pass  # In progress

    def tearDown(self):
        translation.activate(self.old_data['CURRENT_LANGUAGE'])

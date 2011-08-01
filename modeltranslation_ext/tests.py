from django.db import models
from django.test import TestCase
from django.test.utils import override_settings
from django.utils import translation

from modeltranslation import translator

from managers import ml_manager


class TestModel(models.Model):
    untrans = models.CharField(u'untrans', max_length=255)
    trans = models.CharField(u'trans', max_length=255)
    objects = ml_manager(models.Manager)()


class TestTranslationOptions(translator.TranslationOptions):
    fields = ('trans',)

translator.translator._registry = {}
translator.translator.register(TestModel, TestTranslationOptions)


@override_settings(
    LANGUAGE_CODE='ru',
    LANGUAGES=(
        ('ru', u'Russian'),
        ('en', u'English'),
    ),
    USE_I18N=True
)
class ModeltranslationExtTest(TestCase):

    def setUp(self):
        self.data = [
            {'id': 1,
             'untrans': u'untrans1',
             'trans': u'trans1',
             'trans_ru': u'trans1-ru',
             'trans_en': u'trans1-en', },
            {'id': 2,
             'untrans': u'untrans2',
             'trans': u'trans2',
             'trans_ru': u'trans2-ru',
             'trans_en': u'trans2-en', },
            {'id': 3,
             'untrans': u'untrans3',
             'trans': u'trans3',
             'trans_ru': u'trans3-ru',
             'trans_en': u'trans3-en', },
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

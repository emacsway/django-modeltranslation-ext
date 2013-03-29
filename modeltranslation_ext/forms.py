from __future__ import absolute_import, unicode_literals
from django import forms
from django.forms.models import ModelFormMetaclass
from .utils import (formfield_exclude_translations,
    formfield_exclude_original, formfield_exclude_irrelevant, populate_exclude)


class TranslationBase(ModelFormMetaclass):
    def __new__(cls, name, bases, attrs):
        exclude = list(getattr(attrs.get('Meta', None), 'exclude', []))
        if exclude:
            populate_exclude(exclude, attrs['Meta'].model)
            attrs['Meta'].exclude = exclude
        attrs['formfield_callback'] = lambda self, **kw: formfield_exclude_translations(self, **kw)
        return ModelFormMetaclass.__new__(cls, name, bases, attrs)


class TranslationModelForm(TranslationBase(b'NewBase', (forms.ModelForm,), {})):
    """Shows localized form"""
    pass


class TranslationBulkBase(ModelFormMetaclass):
    def __new__(cls, name, bases, attrs):
        exclude = list(getattr(attrs.get('Meta', None), 'exclude', []))
        if exclude:
            populate_exclude(exclude, attrs['Meta'].model)
            attrs['Meta'].exclude = exclude
        attrs['formfield_callback'] = lambda self, **kw: formfield_exclude_original(self, **kw)
        return ModelFormMetaclass.__new__(cls, name, bases, attrs)


class TranslationBulkModelForm(TranslationBulkBase(b'NewBase', (forms.ModelForm,), {})):
    """Shows localized form"""
    pass


class TranslationActualBase(ModelFormMetaclass):
    def __new__(cls, name, bases, attrs):
        exclude = list(getattr(attrs.get('Meta', None), 'exclude', []))
        if exclude:
            populate_exclude(exclude, attrs['Meta'].model)
            attrs['Meta'].exclude = exclude
        attrs['formfield_callback'] = lambda self, **kw: formfield_exclude_irrelevant(self, **kw)
        return ModelFormMetaclass.__new__(cls, name, bases, attrs)


class TranslationActualModelForm(TranslationActualBase(b'NewBase', (forms.ModelForm,), {})):
    """Shows localized form"""
    pass

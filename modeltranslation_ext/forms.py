from __future__ import absolute_import, unicode_literals
from django import forms
from django.forms.models import ModelFormMetaclass
from django.db.models.fields import FieldDoesNotExist
from .utils import (formfield_exclude_translations,
    formfield_exclude_original, formfield_exclude_irrelevant, populate_exclude)


class TranslationBase(ModelFormMetaclass):
    def __new__(cls, name, bases, attrs):
        exclude = list(getattr(attrs.get('Meta', None), 'exclude', []))
        if exclude:
            populate_exclude(exclude, attrs['Meta'].model)
            attrs['Meta'].exclude = exclude
        attrs['formfield_callback'] = formfield_exclude_translations
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
        attrs['formfield_callback'] = formfield_exclude_original
        return ModelFormMetaclass.__new__(cls, name, bases, attrs)


class TranslationBulkModelForm(TranslationBulkBase(b'NewBase', (forms.ModelForm,), {})):
    """Shows localized form"""
    def __init__(self, *args, **kwargs):
        super(TranslationBulkModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            try:
                new_field = formfield_exclude_original(
                    self._meta.model._meta.get_field(name),
                    field=field
                )
            except FieldDoesNotExist:
                new_field = field
            if new_field:
                self.fields[name] = new_field
            else:
                del self.fields[name]


class TranslationActualBase(ModelFormMetaclass):
    def __new__(cls, name, bases, attrs):
        exclude = list(getattr(attrs.get('Meta', None), 'exclude', []))
        if exclude:
            populate_exclude(exclude, attrs['Meta'].model)
            attrs['Meta'].exclude = exclude
        return ModelFormMetaclass.__new__(cls, name, bases, attrs)


class TranslationActualModelForm(TranslationActualBase(b'NewBase', (forms.ModelForm,), {})):
    """Shows localized form"""
    def __init__(self, *args, **kwargs):
        super(TranslationBulkModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            try:
                new_field = formfield_exclude_irrelevant(
                    self._meta.model._meta.get_field(name),
                    field=field
                )
            except FieldDoesNotExist:
                new_field = field
            if new_field:
                self.fields[name] = new_field
            else:
                del self.fields[name]

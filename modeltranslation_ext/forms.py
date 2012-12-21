from __future__ import absolute_import, unicode_literals
from django import forms
from .utils import (formfield_exclude_translations,
    formfield_exclude_original, formfield_exclude_irrelevant)


class TranslationModelForm(forms.ModelForm):
    """Shows localized form"""
    def formfield_callback(self, **kwargs):
        """formfield_exclude_translations implementation"""
        return formfield_exclude_translations(self, **kwargs)


class TranslationBulkModelForm(forms.ModelForm):
    """Shows localized form"""
    def formfield_callback(self, **kwargs):
        """formfield_exclude_translations implementation"""
        return formfield_exclude_original(self, **kwargs)


class TranslationActualModelForm(forms.ModelForm):
    """Shows localized form"""
    def formfield_callback(self, **kwargs):
        """formfield_exclude_translations implementation"""
        return formfield_exclude_irrelevant(self, **kwargs)

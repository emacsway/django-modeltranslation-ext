# -*- coding: utf-8 -*-
from copy import copy

from django import forms, template
from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes import generic

from modeltranslation.settings import *
from django.utils.translation import ugettext, ugettext_lazy as _
from modeltranslation.translator import translator
from modeltranslation.utils import get_translation_fields
# Ensure that models are registered for translation before TranslationAdmin
# runs. The import is supposed to resolve a race condition between model import
# and translation registration in production (see issue 19).
import modeltranslation.models

class TranslationAdminBase(object):
    """
    Mixin class which adds patch_translation_field functionality.
    """
    orig_was_required = {}

    def patch_translation_field(self, db_field, field, **kwargs):
        
        if hasattr(db_field, 'translated_field'):
            field = None
            return None
        
        trans_opts = translator.get_options_for_model(self.model)
        if db_field.name in trans_opts.fields:
            field.widget.attrs['class'] = getattr(field.widget.attrs, 'class', '') + ' language-depended'
            field.help_text = u'{0} {1}'.format(field.help_text, ugettext('This field dependent on current language.'))
        
        # Also we can add here to field.label, that field is language depended. See modeltranslation/admin.py
        #if db_field.name.startswith('body'):
        #    return db_field.formfield(widget=TinyMCE(
        #        attrs={'cols': 80, 'rows': 30},
        #        mce_attrs={} #'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
        #    ))
        return field


class TranslationAdmin(admin.ModelAdmin, TranslationAdminBase):
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        # Call the baseclass function to get the formfield
        field = super(TranslationAdmin, self).formfield_for_dbfield(db_field,
                                                                    **kwargs)
        field = self.patch_translation_field(db_field, field, **kwargs)
        return field

class TranslationTabularInline(admin.TabularInline, TranslationAdminBase):
    def formfield_for_dbfield(self, db_field, **kwargs):
        # Call the baseclass function to get the formfield
        field = super(TranslationTabularInline,
                      self).formfield_for_dbfield(db_field, **kwargs)
        field = self.patch_translation_field(db_field, field, **kwargs)
        return field


class TranslationStackedInline(admin.StackedInline, TranslationAdminBase):
    def formfield_for_dbfield(self, db_field, **kwargs):
        # Call the baseclass function to get the formfield
        field = super(TranslationStackedInline,
                      self).formfield_for_dbfield(db_field, **kwargs)
        field = self.patch_translation_field(db_field, field, **kwargs)
        return field


class TranslationGenericTabularInline(generic.GenericTabularInline,
                                      TranslationAdminBase):
    def formfield_for_dbfield(self, db_field, **kwargs):
        # Call the baseclass function to get the formfield
        field = super(TranslationGenericTabularInline,
                      self).formfield_for_dbfield(db_field, **kwargs)
        field = self.patch_translation_field(db_field, field, **kwargs)
        return field


class TranslationGenericStackedInline(generic.GenericStackedInline,
                                      TranslationAdminBase):
    def formfield_for_dbfield(self, db_field, **kwargs):
        # Call the baseclass function to get the formfield
        field = super(TranslationGenericStackedInline,
                      self).formfield_for_dbfield(db_field, **kwargs)
        field = self.patch_translation_field(db_field, field, **kwargs)
        return field

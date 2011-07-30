# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes import generic
from utils import formfield_exclude_translations


class TranslationAdminBase(object):
    """Shows localized form.

    Mixin class which adds patch_translation_field functionality.
    """
    def patch_translation_field(self, db_field, field, **kwargs):
        """formfield_exclude_translations implementation"""
        return formfield_exclude_translations(db_field, field=field)


class TranslationAdmin(admin.ModelAdmin, TranslationAdminBase):
    """Shows localized form"""
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(TranslationAdmin, self).formfield_for_dbfield(db_field,
                                                                    **kwargs)
        field = self.patch_translation_field(db_field, field, **kwargs)
        return field


class TranslationTabularInline(admin.TabularInline, TranslationAdminBase):
    """Shows localized form"""
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(TranslationTabularInline,
                      self).formfield_for_dbfield(db_field, **kwargs)
        field = self.patch_translation_field(db_field, field, **kwargs)
        return field


class TranslationStackedInline(admin.StackedInline, TranslationAdminBase):
    """Shows localized form"""
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(TranslationStackedInline,
                      self).formfield_for_dbfield(db_field, **kwargs)
        field = self.patch_translation_field(db_field, field, **kwargs)
        return field


class TranslationGenericTabularInline(generic.GenericTabularInline,
                                      TranslationAdminBase):
    """Shows localized form"""
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(TranslationGenericTabularInline,
                      self).formfield_for_dbfield(db_field, **kwargs)
        field = self.patch_translation_field(db_field, field, **kwargs)
        return field


class TranslationGenericStackedInline(generic.GenericStackedInline,
                                      TranslationAdminBase):
    """Shows localized form"""
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(TranslationGenericStackedInline,
                      self).formfield_for_dbfield(db_field, **kwargs)
        field = self.patch_translation_field(db_field, field, **kwargs)
        return field

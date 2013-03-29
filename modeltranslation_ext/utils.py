from __future__ import absolute_import, unicode_literals
from django.utils.translation import ugettext_lazy as _, string_concat
from modeltranslation.translator import translator
from modeltranslation.utils import get_language, build_localized_fieldname


def populate_exclude(exclude, model):
    """handles exclude"""
    trans_opts = translator.get_options_for_model(model)
    for fn in exclude[:]:
        for tf in trans_opts.fields.get(fn, set()):
            print '--', tf.name
            exclude.append(tf.name)
    return exclude


def formfield_exclude_translations(db_field, **kwargs):
    """Filter form and keep only non-localized fields"""
    if hasattr(db_field, 'translated_field'):
        return None

    if 'field' in kwargs:
        field = kwargs['field']
    else:
        field = db_field.formfield(**kwargs)

    if not field:
        return field

    trans_opts = translator.get_options_for_model(db_field.model)
    if db_field.name in trans_opts.fields:
        field.widget.attrs['class'] = '{0} {1}'.format(
            getattr(field.widget.attrs, 'class', ''),
            'language-depended'
        )
        field.help_text = string_concat(
            field.help_text,
            _(' '),
            _('This field dependent on current language.')
        )
    return field


def formfield_exclude_original(db_field, **kwargs):
    """Filter form and keep only localized fields"""
    trans_opts = translator.get_options_for_model(db_field.model)
    if db_field.name in trans_opts.fields:
        return None

    if 'field' in kwargs:
        field = kwargs['field']
    else:
        field = db_field.formfield(**kwargs)

    if hasattr(db_field, 'translated_field'):
        if db_field.name.endswith('_{0}'.format(get_language())):
            field.required = True
        else:
            field.required = False

    return field


def formfield_exclude_irrelevant(db_field, **kwargs):
    """Filter form and keep only localized fields"""
    trans_opts = translator.get_options_for_model(db_field.model)
    if db_field.name in trans_opts.fields:
        return None

    if 'field' in kwargs:
        field = kwargs['field']
    else:
        field = db_field.formfield(**kwargs)

    if hasattr(db_field, 'translated_field'):
        if db_field.name.endswith('_{0}'.format(get_language())):
            field.required = True
            field.widget.attrs['class'] = '{0} {1}'.format(
                getattr(field.widget.attrs, 'class', ''),
                'language-depended'
            )
            field.help_text = string_concat(
                field.help_text,
                _(' '),
                _('This field dependent on current language.')
            )
        else:
            return None

    return field


def localize_fieldname(field_name, lang=None):
    """Localize fieldname"""
    if lang is None:
        lang = get_language()
    return build_localized_fieldname(field_name, lang)

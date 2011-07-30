from django.utils.translation import ugettext_lazy as _, string_concat
from modeltranslation.translator import translator
from modeltranslation.utils import get_language, build_localized_fieldname


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
        field.widget.attrs['class'] = u'{0} {1}'.format(
            getattr(field.widget.attrs, 'class', ''),
            'language-depended'
        )
        field.help_text = string_concat(
            field.help_text,
            _('This field dependent on current language.')
        )
    return field


def localize_fieldname(field_name, lang=None):
    """Localize fieldname"""
    if lang is None:
        lang = get_language()
    return build_localized_fieldname(field_name, lang)

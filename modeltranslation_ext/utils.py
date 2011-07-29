from django.utils.translation import ugettext, ugettext_lazy as _
from modeltranslation.translator import translator
from modeltranslation.utils import get_language, build_localized_fieldname


def formfield_exclude_translations(db_field, **kwargs):
    if hasattr(db_field, 'translated_field'):
        return None
    
    field = db_field.formfield(**kwargs)
    if not field:
        return field
    trans_opts = translator.get_options_for_model(db_field.model)
    if db_field.name in trans_opts.fields:
        field.widget.attrs['class'] = getattr(field.widget.attrs, 'class', '') + ' language-depended'
        field.help_text = u'{0} {1}'.format(field.help_text, ugettext('This field dependent on current language.'))
    
    return field

def localize_fieldname(field_name, lang=None):
    if lang is None:
        lang = get_language()
    return build_localized_fieldname(field_name, lang)


from django import forms
from utils import formfield_exclude_translations


class TranslationModelForm(forms.ModelForm):
    """Shows localized form"""
    def formfield_callback(self, **kwargs):
        """formfield_exclude_translations implementation"""
        return formfield_exclude_translations(self, **kwargs)

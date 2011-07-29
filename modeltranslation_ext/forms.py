from django import forms
from utils import formfield_exclude_translations

class TranslationModelForm(forms.ModelForm):
    
    def formfield_callback(self, **kwargs):
        return formfield_exclude_translations(self, **kwargs)
    
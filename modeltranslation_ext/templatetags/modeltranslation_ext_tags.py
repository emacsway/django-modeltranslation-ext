from __future__ import absolute_import, unicode_literals
from django import template
from ..utils import localize_fieldname as _localize_fieldname

register = template.Library()


@register.filter
def localize_fieldname(name):
    return _localize_fieldname(name)

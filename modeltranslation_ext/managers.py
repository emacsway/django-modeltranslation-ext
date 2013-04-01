from __future__ import absolute_import, unicode_literals
from django.db.models import Q, F
from django.db.models.fields.related import RelatedField
from django.db.models.query import QuerySet

from modeltranslation.translator import translator
from modeltranslation.utils import get_language
from modeltranslation_ext.utils import localize_fieldname

LOOKUP_SEP = '__'


class MultilingualQuerySet(QuerySet):
    """Multilingual QuerySet"""

    def localize_fieldname(self, name, model=None, lang=None):
        """Localizes translatable field name"""
        model = model or self.model
        trans_opts = translator.get_options_for_model(model)
        if name in trans_opts.fields:
            return localize_fieldname(name, lang)
        return name

    def localize_expr(self, expr):
        """Localizes translatable field names in expressions"""
        if isinstance(expr, Q):
            expr.children = map(self.localize_expr, expr.children)
            return expr

        if isinstance(expr, F):
            expr.name = self.localize_expr(expr.name)
            return expr

        if isinstance(expr, tuple) and len(expr) == 2:
            return (self.localize_expr(expr[0]), self.localize_val(expr[1]), )

        if expr == "?":  # ORDER BY RAND()
            return expr

        if expr[0] == '-':
            expr = expr[1:]
            desc = '-'  # ORDER BY ... DESC
        else:
            desc = ''
        parts = expr.split(LOOKUP_SEP)
        parts = self.localize_related(parts)

        return "{0}{1}".format(desc, LOOKUP_SEP.join(parts))

    def localize_related(self, parts, model=None):
        """Localization for related fields"""
        model = model or self.model
        parts = parts[:]
        parts[0] = self.localize_fieldname(parts[0], model)  # name__contains
        if len(parts) > 1:  # related__name or related__name__contains
            if parts[0] in model._meta.get_all_field_names():
                field_object, modelclass, direct, m2m = model._meta.get_field_by_name(parts[0])
                if direct and isinstance(field_object, RelatedField):
                    parts[1:] = self.localize_related(
                        parts[1:], field_object.related.parent_model
                    )
        return parts

    def localize_val(self, val):
        """Localizes translatable field names in values"""
        if isinstance(val, (Q, F, )):
            return self.localize_expr(val)
        return val

    def _translate(self, *args, **kwargs):
        """Localizes field names in args or kwargs"""
        if args:
            return map(self.localize_expr, args)
        else:
            for key in list(kwargs.keys()):
                kwargs[self.localize_expr(key)] = self.localize_val(kwargs.pop(key))
            return kwargs

    def filter(self, *args, **kwargs):
        """Localizes field names in filter method"""
        return super(MultilingualQuerySet, self)\
            .filter(*self._translate(*args), **self._translate(**kwargs))

    def exclude(self, *args, **kwargs):
        """Localizes field names in exclude method"""
        return super(MultilingualQuerySet, self)\
            .exclude(*self._translate(*args), **self._translate(**kwargs))

    def order_by(self, *args):
        """Localizes field names in exclude method"""
        return super(MultilingualQuerySet, self)\
            .order_by(*self._translate(*args))

    def detect_by(self, field):
        """Limited select to current language."""
        loc_field = self.localize_fieldname(field)
        return super(MultilingualQuerySet, self).filter(
            Q(**{"{0}__isnull".format(loc_field): False, }) &\
            ~Q(**{"{0}__exact".format(loc_field): "", })
        )

    def select_fast(self):
        """Speed optimization"""
        # TODO not working, need to fix
        return MultilingualQuerySet(self.model, self.query, self.db)\
            .filter(pk__in=self)


def ml_manager(superclass):
    class MultilingualManager(superclass):
        """Multilingual manager"""

        def get_query_set(self):
            """Returns a new QuerySet object.

            Subclasses can override this method
            to easily customize the behavior of the Manager.
            """
            return MultilingualQuerySet(self.model, using=self._db)

        def localize_fieldname(self, name):
            """Localizes translatable field name"""
            return self.get_query_set().localize_fieldname(name)

        def localize_expr(self, name):
            """Localizes translatable field names in expressions"""
            return self.get_query_set().localize_expr(name)

        def select_fast(self, qs):
            """Speed optimization"""
            return self.get_query_set().filter(pk__in=qs)

        """
        def create(self, **kwargs):
            from django.conf import settings
            langs = [x[0] for x in settings.LANGUAGES]
            lang = get_language()
            langs = dict((l, 1) for l in langs)

            if hasattr(self.model, 'trans_fields'):
                for key in kwargs.keys():
                    if key in self.model.trans_fields:
                        val = kwargs.pop(key)
                        for l in langs:
                            if not langs.has_key(l + '_' + key):
                                kwargs[l + '_' + key] = val

            return super(MultilingualManager, self).create(**kwargs)
        """
    return MultilingualManager


def pb_manager(superclass):
    class PublishManager(superclass):
        """
            Includes only objects marked as publish on current
        """
        def get_query_set(self):
            name = get_language() + '_publish'
            return super(PublishManager, self).get_query_set()\
                .filter(**{str(name): True})
    return PublishManager

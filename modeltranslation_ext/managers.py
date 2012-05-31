from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models.sql.constants import LOOKUP_SEP

from modeltranslation.translator import translator
from modeltranslation.utils import get_language
from modeltranslation_ext.utils import localize_fieldname


class MultilingualQuerySet(QuerySet):
    """Multilingual QuerySet"""

    def localize_fieldname(self, name, lang=None):
        """Localizes translatable field name"""
        trans_opts = translator.get_options_for_model(self.model)
        if name in trans_opts.fields:
            return localize_fieldname(name, lang)
        return name

    def localize_expr(self, name):
        """Localizes translatable field names in expressions"""
        if isinstance(name, Q):
            name.children = list(name.children)
            for i, v in enumerate(name.children):
                if isinstance(v, Q):
                    name.children[i] = self.localize_expr(v)
                else:
                    name.children[i] = (self.localize_expr(v[0]), v[1], )
            return name

        if name[0] == '-':
            name = name[1:]
            desc = '-'  # ORDER BY ... DESC
        else:
            desc = ''
        parts = name.split(LOOKUP_SEP)
        parts[0] = self.localize_fieldname(parts[0])
        # TODO supports relations
        return "{0}{1}".format(desc, LOOKUP_SEP.join(parts))

    def _translate(self, *args, **kwargs):
        """Localizes field names in args or kwargs"""
        trans_opts = translator.get_options_for_model(self.model)

        if (args):
            args = list(args)
            for i, v in enumerate(args):
                args[i] = self.localize_expr(v)
            return args
        else:
            for key in kwargs.keys():
                new_key = self.localize_expr(key)
                kwargs[new_key] = kwargs.pop(key)
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

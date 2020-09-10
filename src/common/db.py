import collections

import inflect
from sqlalchemy import inspect, or_, and_

from .. import db
from ..common.cleaner import Cleaner
from ..common.error import *


class DB:
    # Helpers

    @classmethod
    def _query_builder(cls, model, filters=[], expand=[], include=[], sort_by=None, limit=None, offset=None):
        query = db.session.query(model)
        for logic_operator, filter_arr in filters:
            criterion = []
            for key, value in filter_arr:
                if key == 'like':
                    for like_k, like_v in value:
                        search = "%{}%".format(like_v)
                        criterion.append(like_k.like(search))
                if key == 'equal':
                    for equal_k, equal_v in value:
                        criterion.append(equal_k == equal_v)
                if key == 'gt':
                    for gt_k, gt_v in value:
                        criterion.append(gt_k > gt_v)
                if key == 'gte':
                    for gte_k, gte_v in value:
                        criterion.append(gte_k >= gte_v)
                if key == 'lt':
                    for lt_k, lt_v in value:
                        criterion.append(lt_k < lt_v)
                if key == 'lte':
                    for lte_k, lte_v in value:
                        criterion.append(lte_k <= lte_v)
            if logic_operator == 'or':
                query = query.filter(or_(*criterion))
            if logic_operator == 'and':
                query = query.filter(and_(*criterion))
        for i, k in enumerate(expand):
            tables = k.split('.')
            for j, table in enumerate(tables):
                if j == 0:
                    # query = query.join(getattr(model, table))
                    options = db.lazyload(getattr(model, table))
                else:
                    nested_class = cls.get_class_by_tablename(tables[j - 1])
                    # query = query.join(getattr(nested_class, table))
                    options = options.lazyload(getattr(nested_class, table))
            if i == len(expand) - 1:
                query = query.options(options)
        for i, k in enumerate(include):
            tables = k.split('.')
            for j, table in enumerate(tables):
                if j == 0:
                    # query = query.join(getattr(model, table))
                    options = db.joinedload(getattr(model, table))
                else:
                    nested_class = cls.get_class_by_tablename(cls._singularize(tables[j - 1]))
                    # query = query.join(getattr(nested_class, table))
                    options = options.joinedload(getattr(nested_class, table))
            if i == len(include) - 1:
                query = query.options(options)
        if sort_by is not None:
            direction = re.search('[.](a|de)sc', sort_by)
            if direction is not None:
                direction = direction.group()
            key = sort_by.split(direction)[0]
            if direction == '.asc':
                query = query.order_by(getattr(model, key).asc())
            elif direction == '.desc':
                query = query.order_by(getattr(model, key).desc())
            else:  # for now, lack of a direction will be interpreted as asc
                query = query.order_by(getattr(model, key).asc())
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return query

    @classmethod
    def get_class_by_tablename(cls, tablename):
        for c in db.Model._decl_class_registry.values():
            if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
                return c

    @classmethod
    def _is_pending(cls, instance):
        inspection = inspect(instance)
        return inspection.pending

    @classmethod
    def _get_cache_key(cls, model, query):
        return f"{model.__tablename__}:{str(query)}"

    @classmethod
    def _pluralize(cls, tablename):
        p = inflect.engine()
        return p.plural_noun(tablename)

    @classmethod
    def _singularize(cls, tablename):
        p = inflect.engine()
        return p.singular_noun(tablename)

    @classmethod
    # Methods
    def init(cls, model, **kwargs):
        return model(**kwargs)

    @classmethod
    def count(cls, model):
        return db.session.query(model).count()

    @classmethod
    def save(cls, instance):
        if not instance:
            raise MissingParamError(instance.__tablename__)
        if not Cleaner.is_mapped(instance):
            raise InvalidTypeError(instance.__tablename__, 'mapped')

        if not cls._is_pending(instance):
            db.session.add(instance)

        db.session.commit()
        return instance

    @classmethod
    # TODO: Consider using dataclass instead of a named tuple
    def find(cls, model, page=None, per_page=None, expand=[], include=[], nested={}, search={}, **kwargs):
        filters = []
        for k, v in kwargs.items():
            filters.append(
                (
                    'and',
                    [
                        ('equal', [(getattr(model, k), v)])
                    ]
                )
            )

        for k, v in nested.items():
            nested_class = cls.get_class_by_tablename(k)
            for nested_k, nested_v in v.items():
                filters.append(
                    (
                        'and',
                        [
                            ('equal', [(getattr(nested_class, nested_k), nested_v)])
                        ]
                    )
                )

        if 'key' in search:
            filters.append(
                (
                    'or',
                    [
                        (
                            'like',
                            [
                                (getattr(model, field), search['key'])
                            ]
                        ) for field in search['fields']
                    ]
                )
            )

        query = cls._query_builder(model=model, filters=filters, include=include, expand=expand)

        if page is not None and per_page is not None:
            paginate = query.paginate(page, per_page, False)
            items = paginate.items
            total = paginate.total
        else:
            items = query.all()
            total = len(items)

        Find = collections.namedtuple('Find', ['items', 'total'])
        return Find(items=items, total=total)

    @classmethod
    def destroy(cls, instance):
        db.session.delete(instance)
        db.session.commit()
        return True

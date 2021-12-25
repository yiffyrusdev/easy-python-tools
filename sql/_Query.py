from typing import Iterable, Union
from ._Table import *
from ._internal import proper_values
from ._Where import *


class UpdateQuery:
    def __init__(self, target: 'Table', fields: Iterable['TableField'], values: Iterable, where: 'Where' = None):
        pass


class SelectQuery:
    def __init__(self, source: 'Table', fields: Iterable['TableField'], where: 'Where' = None, distinct=False):
        self._source = source
        self._fields = tuple(fields)
        self._distinct = distinct
        self._where = where
        self._body = None

    @property
    def source(self) -> 'Table':
        return self._source

    @property
    def fields(self) -> tuple['TableField']:
        return self._fields

    @property
    def body(self):
        return self._body

    @property
    def distinct(self) -> 'SelectQuery':
        return SelectQuery(self.source, fields=self.fields, where=self._where, distinct=True)

    def __eq__(self, values) -> 'SelectQuery':
        if not isinstance(values, tuple):
            values = (values,)
        values = proper_values(values)

        new_wheres = []
        for field, cmp in zip(self.fields, values):
            new_wheres.append(WhereEq(field, cmp))
        if self._where is None:
            new_where = WhereAND(*new_wheres)
        else:
            new_where = WhereAND(self._where, *new_wheres)

        return SelectQuery(self.source, fields=self.fields, where=new_where)

    def __or__(self, values) -> 'SelectQuery':
        if not isinstance(values, tuple):
            values = (values,)
        values = proper_values(values)

        new_wheres = []
        for field, cmp in zip(self.fields, values):
            new_wheres.append(WhereEq(field, cmp))
        if self._where is None:
            new_where = WhereOR(*new_wheres)
        else:
            new_where = WhereOR(self._where, *new_wheres)

        return SelectQuery(self.source, fields=self.fields, where=new_where)

    def __call__(self, force=False):
        if (self.body is None) or force:
            query = str(self)
            self._body = self.source.db.query(query, commit=False).fetchall()

        return self.body

    def __str__(self):
        select = f'''SELECT {"DISTINCT" if self._distinct else ""}
        {",".join(f.full_name for f in self.fields)} 
        FROM {self.source.query}'''
        where = f'WHERE {self._where}' if self._where is not None else ""

        query = f'{select} {where};'
        return query

    def __repr__(self) -> str:
        return str(self)

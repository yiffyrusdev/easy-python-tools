from typing import Iterable
from ._Table import *
from ._internal import proper_values


class UpdateQuery:
    def __init__(self, target: 'Table', fields: Iterable[str], values: Iterable, where: Iterable[str] = None):
        pass


class SelectQuery:
    def __init__(self, source: 'Table', fields: Iterable[str] = None, where: Iterable[str] = None):
        self._source = source
        self._fields = (*fields,) if fields is not None else tuple(source.fields.keys())
        self._where = (*where,) if where is not None else ()
        self._body = None

    @property
    def source(self) -> 'Table':
        return self._source

    @property
    def fields(self) -> tuple[str]:
        return self._fields

    @property
    def body(self):
        return self._body

    def __eq__(self, values) -> 'SelectQuery':
        if not isinstance(values, tuple):
            values = (values,)
        values = proper_values(values)

        new_where = []
        for field, cmp in zip(self.fields, values):
            if cmp != 'NULL':
                new_where.append(f'{field} = {cmp}')
        new_where = tuple(new_where)

        return SelectQuery(self.source, fields=self.fields, where=self._where+new_where)

    def __call__(self, force=False):
        if (self.body is None) or force:
            query = str(self)
            self._body = self.source.db.query(query, commit=False).fetchall()

        return self.body

    def __str__(self):
        select = f'SELECT {",".join(self.fields)} FROM {self.source.query}'
        where = ''
        if self._where:
            where = f'WHERE {" AND ".join(self._where)}'

        query = f'{select} {where};'
        return query

    def __repr__(self) -> str:
        return str(self)

from typing import Iterable, Union
import sql._Table as _Table
import sql._Where as _Where


class UpdateQuery:
    def __init__(self, target: '_Table.Table', fields: Iterable['_Table.TableField'], values: Iterable, where: '_Where.Where' = None):
        pass


class SelectQuery:
    def __init__(self, source: '_Table.Table', fields: Iterable['_Table.TableField'], where: _Where.Where = None, distinct=False):
        self._source = source
        self._fields = tuple(fields)
        self._distinct = distinct
        self._where = where
        self._body = None

    @property
    def source(self) -> '_Table.Table':
        return self._source

    @property
    def fields(self) -> tuple['_Table.TableField']:
        return self._fields

    @property
    def body(self):
        return self._body

    @property
    def distinct(self) -> 'SelectQuery':
        return SelectQuery(self.source, fields=self.fields, where=self._where, distinct=True)

    def __eq__(self, values: list | tuple) -> 'SelectQuery':
        if isinstance(values, list):
            where_type = _Where.WhereAND
        elif isinstance(values, tuple):
            where_type = _Where.WhereOR
        else:
            raise TypeError(f'expected <tuple> for AND or <list> for OR, got {type(values)}')

        new_wheres = []
        for value, field in zip(values, self.fields):
            if isinstance(value, tuple):
                new_where = _Where.WhereOR(*(_Where.WhereEq(field, v) for v in value))
            elif isinstance(value, list):
                new_where = _Where.WhereAND(*(_Where.WhereEq(field, v) for v in value))
            else:
                new_where = _Where.WhereEq(field, value)

            new_wheres.append(new_where)

        where = where_type(*new_wheres)

        return SelectQuery(self.source, self.fields, where=where, distinct=self._distinct)

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

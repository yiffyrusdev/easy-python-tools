from typing import Iterable, Union, Type
import sql._Table as _Table
import sql._Where as _Where
import sql._internal as _internal
import sql._exceptions as _exceptions


class UpdateQuery:
    """
    UpdateQuert object to perform update on table.
    """
    def __init__(self, target: '_Table.Table', fields: Iterable['_Table.TableField'], values: tuple | dict, where: Type['_Where.Where'] = None, group: tuple['_Table.TableField'] = ()):
        self._target = target
        self._fields = fields
        self._values = values
        self._where = where
        self._group = group

        if (not self._target.is_real) and (self._where is not None):
            raise _exceptions.TableIsNotReal(self._target.name)

    def __call__(self, commit=True) -> None:
        """
        Make SQL UPDATE Query, which is presented by current object.

        :param commit: True means to commit changes to database after query success.
        """
        query = str(self)
        self._target.db.query(query, commit=commit)

    def __str__(self) -> str:
        if isinstance(self._values, tuple):
            fields = (f.name for f in self._fields)
            values = self._values
        elif isinstance(self._values, dict):
            fields = (self._target.field_by_name(f).name for f in self._values.keys())
            values = self._values.values()
        else:
            raise TypeError(f'expected <dict> or <tuple> for value assignment, got {type(self._values)}')

        update = f'''UPDATE
        {self._target.name} SET {",".join(fields)} = ({",".join(_internal.proper_values(values))})'''
        where = f' WHERE {self._where}' if self._where is not None else ""
        group = f' GROUP BY {",".join(f.full_name for f in self._group)}' if self._group else ""
        return f'{update}{where}{group};'

    def __repr__(self) -> str:
        return str(self)


class SelectQuery:
    """
    SelectQuery object to perform SELECT queries and its compositions.
    """
    def __init__(self, source: '_Table.Table', fields: Iterable['_Table.TableField'], where: Type['_Where.Where'] = None, group: tuple['_Table.TableField'] = ()):
        self._source = source
        self._fields = tuple(fields)
        self._distinct = False
        self._where = where
        self._body = None
        self._union_comparator = _Where.WhereAND
        self._group = group

    @property
    def union_comparator(self) -> Type['_Where.WhereComposition']:
        """Comparator type which will be used on further conditions composition for this query."""
        return self._union_comparator

    @union_comparator.setter
    def union_comparator(self, value: Type['_Where.WhereComposition']):
        self._union_comparator = value

    @property
    def is_distinct(self) -> bool:
        """Is this query DISTINCT or not."""
        return self._distinct

    @is_distinct.setter
    def is_distinct(self, value: bool):
        self._distinct = value

    @property
    def source(self) -> '_Table.Table':
        """Source Table object to SELECT from."""
        return self._source

    @property
    def fields(self) -> tuple['_Table.TableField']:
        """Fields used in current selection."""
        return self._fields

    @property
    def body(self):
        """Last query operation result. Used for caching."""
        return self._body

    @property
    def distinct(self) -> 'SelectQuery':
        """Make new SelectQuery, which is copy of current, but selection will be DISTINCT."""
        query = SelectQuery(self.source, fields=self.fields, where=self._where)
        query.is_distinct = True
        return query

    @property
    def OR(self) -> 'SelectQuery':
        """Make new SelectQuery, which is copy of current, but newly added selection conditions will be added with OR."""
        query = SelectQuery(self.source, fields=self.fields, where=self._where)
        query.is_distinct = self._distinct
        query.union_comparator = _Where.WhereOR
        return query

    @property
    def AND(self) -> 'SelectQuery':
        """Make new SelectQuery, which is copy of current, but newly added selection conditions will be added with AND."""
        query = SelectQuery(self.source, fields=self.fields, where=self._where)
        query.is_distinct = self._distinct
        query.union_comparator = _Where.WhereAND
        return query

    def WHERE(self, values: list | tuple, comparison: type, union: type) -> 'SelectQuery':
        """
        Make new SelectQuery, which is copy of current, but add new selection condition.

        :param values: condition description.
        :param comparison: Where class reference which represents how values would be checked.
        :param union: WhereComposition class reference which represents how all checks will be composited.
        :return: new SelectQuery object.
        """
        if isinstance(values, list):
            where_type = _Where.WhereAND
        elif isinstance(values, tuple):
            where_type = _Where.WhereOR
        else:
            raise TypeError(f'expected <tuple> for AND or <list> for OR, got {type(values)}')

        new_wheres = []
        for value, field in zip(_internal.proper_values(values), self.fields):
            if (value == tuple()) or (value == list()):
                continue
            if isinstance(value, tuple):
                new_where = _Where.WhereOR(*(comparison(field, v) for v in _internal.proper_values(value)))
            elif isinstance(value, list):
                new_where = _Where.WhereAND(*(comparison(field, v) for v in _internal.proper_values(value)))
            else:
                new_where = comparison(field, value)

            new_wheres.append(new_where)

        where = union(self._where,where_type(*new_wheres)) if self._where is not None else where_type(*new_wheres)

        query = SelectQuery(self.source, self.fields, where=where)
        query.is_distinct = self._distinct
        return query

    def WHERE_EQ(self, values: list | tuple) -> 'SelectQuery':
        """Make new SelectQuery, which is copy of current, but with additional selection condition on equalities."""
        return self.WHERE(values, _Where.WhereEq, self._union_comparator)

    def WHERE_GT(self, values: list | tuple) -> 'SelectQuery':
        """Make new SelectQuery, which is copy of current, but with additional selection condition on greaters."""
        return self.WHERE(values, _Where.WhereGt, self._union_comparator)

    def WHERE_LT(self, values: list | tuple) -> 'SelectQuery':
        """Make new SelectQuery, which is copy of current, but with additional selection condition on lessers."""
        return self.WHERE(values, _Where.WhereLt, self._union_comparator)

    def GROUPBY(self, fields: tuple) -> 'SelectQuery':
        """Make new SelectQuery, which copy of current, but with grouping fields."""
        fields = tuple(self._source.field_by_name(v) for v in fields)
        return SelectQuery(self._source, self._fields, self._where, fields)

    def UPDATE(self, values: tuple | list) -> 'UpdateQuery':
        """Make new UpdateQuery, that affects rows and fields selected with current SelectQuery."""
        if not isinstance(values, dict) and ((lv := len(values)) != (lf := len(self._fields))):
            raise ValueError(f'All fields from selection have to be initialized in UPDATE query, but only {lv} of {lf} are.')
        return UpdateQuery(self._source, self._fields, values, where=self._where, group=self._group)

    def __eq__(self, values: list | tuple) -> 'SelectQuery':
        """Make new SelectQuery, which is copy of current, but with additional selection condition on equalities."""
        return self.WHERE_EQ(values)

    def __gt__(self, values: list | tuple) -> 'SelectQuery':
        """Make new SelectQuery, which is copy of current, but with additional selection condition on greaters."""
        return self.WHERE_GT(values)

    def __lt__(self, values: list | tuple) -> 'SelectQuery':
        """Make new SelectQuery, which is copy of current, but with additional selection condition on lessers."""
        return self.WHERE_LT(values)

    def __mod__(self, fields: tuple) -> 'SelectQuery':
        """Make new SelectQuery, which copy of current, but with grouping fields."""
        return self.GROUPBY(fields)

    def __lshift__(self, values: tuple | dict) -> 'UpdateQuery':
        """Make new UpdateQuery, that affects rows and fields selected with current SelectQuery."""
        return self.UPDATE(values)

    def __call__(self) -> list[tuple]:
        """
        Get result of SQL query, which is presented by current object.

        :param force: True means not to use last cached result.
        :return: select SQL query result or last cached result.
        """
        query = str(self)
        self._body = self._source.db.query(query, commit=False).fetchall()

        return self._body

    def __str__(self):
        select = f'''SELECT {"DISTINCT" if self._distinct else ""}
        {",".join(f.full_name for f in self.fields)} 
        FROM {self.source.query}'''
        where = f' WHERE {self._where}' if self._where is not None else ""
        group = f' GROUP BY {",".join(f.full_name for f in self._group)}' if self._group else ""

        query = f'{select}{where}{group};'
        return query

    def __repr__(self) -> str:
        return str(self)

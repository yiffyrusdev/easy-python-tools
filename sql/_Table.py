from typing import Iterable
from ._Base import *
from ._Query import *


class Table:
    def __init__(self, table_name: str, db_obj: 'Base', table_query: str=None, binded_tables: Iterable['Table']=None):
        self._name = table_name
        self._query = table_name if table_query is None else table_query
        self._is_real = binded_tables is None
        self._db = db_obj
        self._binded = {self} if self.is_real else set()
        if binded_tables is not None:
            for rqt in binded_tables:
                self._binded.update(rqt.binded)

        self._fields = dict()
        self._foreign_keys = dict()
        for rqt in self.binded:
            self._fields.update(db_obj.table_fields(rqt))
            self._foreign_keys.update(db_obj.table_foreign_keys(rqt))

        self._foreign_tables = set()
        for f, fk in self.foreign_keys.items():
            self._foreign_tables.add(fk.master_field.table)

    def field_by_name(self, field_name: str) -> 'TableField':
        return self._fields[f'{self.name}.{field_name}']

    def field_from_name(self, field_name: str) -> str:
        for try_table in self.binded:
            if (fname := f'{try_table.name}.{field_name}') in self.fields:
                return fname
        raise KeyError(f"{self} has no field {field_name}")

    def has_field(self, field_name: str) -> bool:
        for try_table in self.binded:
            if (fname := f'{try_table.name}.{field_name}') in self.fields:
                return True
        return False

    @property
    def is_real(self) -> bool:
        return self._is_real

    @property
    def name(self) -> str:
        return self._name

    @property
    def query(self) -> str:
        return self._query

    @property
    def binded(self) -> set['Table']:
        return self._binded

    @property
    def db(self) -> 'DBase':
        return self._db

    @property
    def fields(self) -> dict['TableField']:
        return self._fields.copy()

    @property
    def foreign_keys(self) -> dict[str, 'TableFK']:
        return self._foreign_keys

    @property
    def foreign_tables(self) -> set['Table']:
        return self._foreign_tables.copy()

    def __getitem__(self, field_names) -> 'SelectQuery':
        if isinstance(field_names, slice):
            field_names = tuple(self.fields.keys())

        if not isinstance(field_names, tuple):
            field_names = (field_names,)
        fields = []
        for f in field_names:
            if f not in self.fields:
                fields.append(self.field_from_name(f))
            else:
                fields.append(f)

        return SelectQuery(self, fields=fields)

    def __mul__(self, other: 'Table') -> 'Table':
        name = f'{self.name}_x_{other.name}'
        binded = self.binded.union(other.binded)
        query = f'({self.query},{other._query})'

        return Table(name, self._db, table_query=query, binded_tables=binded)

    def __and__(self, other: 'Table') -> 'Table':
        if maybe := self.binded.intersection(other.foreign_tables):
            name = f'{other.name}_j_{self.name}'
            master = self
            slave = other
        elif maybe := other.binded.intersection(self.foreign_tables):
            name = f'{self.name}_j_{other.name}'
            master = other
            slave = self
        else:
            raise KeyError(f"{self} and {other} could not be joined")

        for fk, fkey in slave.foreign_keys.items():
            if self.has_field(fkey.master_field.name):
                master_ref = master.field_from_name(fkey.master_field.name)
                slave_ref = slave.field_from_name(fkey.slave_field.name)

        binded = self.binded.union(other.binded)
        query = f'({self.query} INNER JOIN {other.query} ON {master_ref} = {slave_ref})'

        return Table(name, self.db, table_query=query, binded_tables=binded)

    def __repr__(self) -> str:
        return f'Table<{self.name} of {self.db.name}>'

    def __eq__(self, other: 'Table'):
        return (self.query == other.query) and (self.db.name == other.db.name)

    def __hash__(self):
        return hash((self.query, self.db.name))


class TableField:
    def __init__(self, i: int, name: str, typ: str, table_obj: Table):
        self.id = i
        self.name = name
        self.type = typ
        self.table = table_obj

    def __repr__(self) -> str:
        return f'Field<{self.id}, {self.name}, {self.type} of {self.table}>'

    def __eq__(self, other: 'TableField') -> bool:
        return (self.name == other.name) and (self.table == other.table)

    def __hash__(self):
        return hash((self.name, self.table.name, self.table.db.name))


class TableFK:
    def __init__(self, master_field: TableField, slave_field: TableField):
        self.master_field = master_field
        self.slave_field = slave_field

    def __repr__(self) -> str:
        return f'TableFK<{self.slave_field} -> {self.master_field}>'

    def __eq__(self, other: 'TableFK'):
        return (self.master_field == other.master_field) and (self.slave_field == other.slave_field)

    def __hash__(self):
        return hash((self.master_field, self.slave_field))
import sqlite3
from typing import Iterable, Union

import sql._exceptions as _exceptions
import sql._Table as _Table
import sql._internal as _internal


class DBase:
    def __init__(self, dbfile: str):
        self._db_file = dbfile

        self._db_connection = sqlite3.connect(self._db_file)
        self._db_cursor = self._db_connection.cursor()

        self._db_tables = self.get_tables()
        self._active_tables: dict[str, '_Table.Table'] = dict()

    def table(self, table_name: str) -> '_Table.Table':
        if self.has_table(table_name):
            if table_name in self._active_tables:
                table = self._active_tables[table_name]
            else:
                table = _Table.Table(table_name, self)
                self._active_tables[table_name] = table
            return table
        else:
            raise _exceptions.TableNotFound(table_name, self.name)

    def new_table(self, table_name: str, fields: dict) -> '_Table.Table':
        if self.has_table(table_name):
            raise _exceptions.TableAlreadyExists(table_name, self.name)
        else:
            fields = f'{", ".join(f"{k} {v}" for k, v in fields.items())}'
            query = f'CREATE TABLE {table_name}({fields});'
            print(query)
            self.query(query)
            self._db_connection.commit()

            self._db_tables = self.get_tables()

            return self.table(table_name)

    def query(self, query: str, commit=False):
        res = self._db_cursor.execute(query)
        if commit:
            self._db_connection.commit()
        return res

    def select(self, source: str, fields: Iterable[str]):
        return self.query(f'SELECT {",".join(fields)} FROM {source};').fetchall()

    def insert(self, target: str, fields: Iterable[str], values: Iterable):
        f_names = []
        f_values = []
        for f, v in zip(fields, _internal.proper_values(values)):
            if v == "NULL":
                continue
            f_names.append(f)
            f_values.append(v)

        self.query(f'INSERT INTO {target}({",".join(f_names)}) VALUES({",".join(f_values)});', commit=True)
        self._db_connection.commit()

    def has_tables(self, tables: Iterable[Union[str, '_Table.Table']]) -> bool:
        for table in tables:
            if not self.has_table(table):
                return False
        return True

    def has_table(self, table_name: Union[str,'_Table.Table']) -> bool:
        table_name = table_name if isinstance(table_name, str) else table_name.name
        return table_name in self._db_tables

    def get_tables(self) -> set[str]:
        tables = self.query('SELECT name from sqlite_master where type="table"').fetchall()
        return set(t[0] for t in tables)

    def get_fields(self, table: str) -> dict[str, '_Table.TableField']:
        if not self.has_table(table):
            raise _exceptions.TableNotFound(table, self.name)

        table = self.table(table)
        return self.table_fields(table)

    def get_foreign_keys(self, table: str) -> dict[str, '_Table.TableFK']:
        if not self.has_table(table):
            raise _exceptions.TableNotFound(table, self.name)

        table = self.table(table)
        return self.table_foreign_keys(table)

    def table_satisfied(self, table: '_Table.Table') -> bool:
        return self.has_tables(table.binded)

    def tables_satified(self, tables: Iterable['_Table.Table']) -> bool:
        for t in tables:
            return self.table_satisfied(t)
        return True

    def table_fields(self, table: '_Table.Table') -> dict[str, '_Table.TableField']:
        result = self.query(f'PRAGMA table_info({table.query})').fetchall()
        fields = dict((f"{table.name}.{name}", _Table.TableField(i, name, typ, table, is_primary=(pk != 0))) for i,name,typ,_,_,pk in result)

        return fields

    def table_foreign_keys(self, table: '_Table.Table') -> dict[str, '_Table.TableFK']:
        result = self.query(f'PRAGMA foreign_key_list({table.query})').fetchall()
        keys = dict()

        for f in result:
            master = self.table(f[2])
            fk = _Table.TableFK(master.field_by_name(f[4]), table.field_by_name(f[3]))
            keys[f'{table.name}.{fk.slave_field.name}'] = fk

        return keys

    @property
    def name(self) -> str:
        return self._db_file

    @property
    def tables(self) -> set[str]:
        return self._db_tables

    @property
    def active_tables(self) -> dict[str, '_Table.Table']:
        return self._active_tables.copy()

    def __repr__(self) -> str:
        return f'DBase<{self.name}>'

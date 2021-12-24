import sqlite3
from typing import Iterable

from ._exceptions import TableNotFound, TableAlreadyExists
from ._Table import Table, TableField, TableFK


class DBase:
    def __init__(self, dbfile: str):
        self._db_file = dbfile

        self._db_connection = sqlite3.connect(self._db_file)
        self._db_cursor = self._db_connection.cursor()

        self._db_tables = self.get_tables()
        self._active_tables: dict[str, Table] = dict()

    def table(self, table_name: str) -> Table:
        if self.has_table(table_name):
            if table_name in self._active_tables:
                table = self._active_tables[table_name]
            else:
                table = Table(table_name, self)
                self._active_tables[table_name] = table
            return table
        else:
            raise TableNotFound(table_name, self.name)

    def new_table(self, table_name: str, fields: dict) -> Table:
        if self.has_table(table_name):
            raise TableAlreadyExists(table_name, self.name)
        else:
            fields = f'{", ".join(f"{k} {v}" for k, v in fields.items())}'
            query = f'CREATE TABLE {table_name}({fields});'
            print(query)
            self._db_cursor.execute(query)
            self._db_connection.commit()

            self._db_tables = self.get_tables()

            return self.table(table_name)

    def select(self, source: str, fields: Iterable[str]):
        return self._db_cursor.execute(f'SELECT {",".join(fields)} FROM {source};').fetchall()

    def insert(self, target: str, fields: Iterable[str], values: Iterable):
        fields = f'{",".join(fields)}'
        proper_values = []
        for v in values:
            if isinstance(v, str):
                proper_values.append(f'"{v}"')
            else:
                proper_values.append(str(v))
        values = f'{",".join(proper_values)}'

        self._db_cursor.execute(f'INSERT INTO {target}({fields}) VALUES({values});')
        self._db_connection.commit()

    def has_tables(self, tables: Iterable[str | Table]) -> bool:
        for table in tables:
            if not self.has_table(table):
                return False
        return True

    def has_table(self, table_name: str | Table) -> bool:
        table_name = table_name if isinstance(table_name, str) else table_name.name
        return table_name in self._db_tables

    def get_tables(self) -> set[str]:
        tables = self._db_cursor.execute('SELECT name from sqlite_master where type="table"').fetchall()
        return set(t[0] for t in tables)

    def get_fields(self, table: str) -> dict[str, TableField]:
        if not self.has_table(table):
            raise TableNotFound(table, self.name)

        table = self.table(table)
        return self.table_fields(table)

    def get_foreign_keys(self, table: str) -> dict[str, TableFK]:
        if not self.has_table(table):
            raise TableNotFound(table, self.name)

        table = self.table(table)
        return self.table_foreign_keys(table)

    def table_satisfied(self, table: Table) -> bool:
        return self.has_tables(table.binded)

    def tables_satified(self, tables: Iterable[Table]) -> bool:
        for t in tables:
            return self.table_satisfied(t)
        return True

    def table_fields(self, table: Table) -> dict[str, TableField]:
        result = self._db_cursor.execute(f'PRAGMA table_info({table.query})').fetchall()
        fields = dict((f"{table.name}.{name}", TableField(i, name, typ, table)) for i,name,typ,_,_,_ in result)
        return fields

    def table_foreign_keys(self, table: Table) -> dict[str, TableFK]:
        result = self._db_cursor.execute(f'PRAGMA foreign_key_list({table.query})').fetchall()
        keys = dict()

        for f in result:
            master = self.table(f[2])
            fk = TableFK(master.field_by_name(f[4]), table.field_by_name(f[3]))
            keys[f'{table.name}.{fk.slave_field.name}'] = fk

        return keys

    @property
    def name(self):
        return self._db_file

    def __repr__(self) -> str:
        return f'DBase<{self.name}>'

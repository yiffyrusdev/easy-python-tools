from typing import Sequence, Mapping, Collection, Any
from . import _Table
from . import _Base


def base_to_dict(base: '_Base.DBase') -> dict[str, list[dict[str, Any]]]:
    tables = dict()
    for t_name in base.tables:
        t = base.table(t_name)
        tables.update({t_name: table_to_list(t)})

    return tables


def table_to_list(table: '_Table.Table') -> list[dict[str, Any]]:
    query = table[:]
    fields = [f.name for f in query.fields]
    body = query()

    rows = [dict(zip(fields, row)) for row in body]
    return rows


def table_to_schema(table: '_Table.Table') -> dict[str, str]:
    schema = dict()
    for f in table.fields.values():
        signature = f'{f.type} {"NOT NULL" if not f.is_nullable else ""} {"PRIMARY KEY" if f.is_primary else ""}'
        schema.update({f.name: signature})

    for f in table.foreign_keys.values():
        key = f'foreign key({f.slave_field.name})'
        signature = f'references {f.master_field.table.name}({f.master_field.name})'
        schema.update({key: signature})

    return schema


def map_to_base(db_name: str, data_map: Mapping[str, Sequence[Mapping[str, Any]]], primary_fields: Mapping[str, str]) -> '_Base.DBase':
    """
    Create DBase from data mapping.

    data mapping entry must have following structure:
        Table_name: <Sequence of instance mappings <Field_name: Instance_value>>

    :param db_name: database filename
    :param data_map: data mapping
    :param primary_fields: mapping for spec primary key fields <Table_name: Primaryfield_name>
    """
    db = _Base.DBase(db_name)
    for table_name, table_data in data_map.items():
        pk = primary_fields[table_name] if table_name in primary_fields else None
        seq_to_table(db, table_name, table_data, primary_field=pk)

    return db


def seq_to_table(db: '_Base.DBase', name: str, rows: Sequence[Mapping[str, Any]], primary_field: str = None, ignore_fields: Collection[str] = tuple()) -> '_Table.Table':
    """
    Create new Table in existing DBase from data mapping sequence.

    Each map in sequence - is a row instance.
    Row instance map entry must have following structure:
        Field_name: Instance_vale_for_field

    :param db: DBase object instance
    :param name: name for the new table
    :param rows: sequence of data mappings containing row instances for table
    :param primary_field: name of field which will be primary
    :param ignore_fields: sequence of field names to ignore
    """
    schema = seq_to_schema(rows, primary_field=primary_field, ignore_fields=ignore_fields)
    table = db.new_table(name, schema)

    for row in rows:
        table.INSERT(row)

    return table


def seq_to_schema(rows: Sequence[Mapping[str, Any]], primary_field: str = None, ignore_fields: Collection[str] = tuple()) -> dict:
    """
    Create Table SQL schema from data mapping sequence.

    Each map in sequence - is a row instance.
    Row instance map entry must have following structure:
        Field_name: Instance_vale_for_field

    :param rows: sequence of data mappings containing row instances for table
    :param primary_field: name of field which will be primary
    :param ignore_fields: sequence of field names to ignore
    """
    schema = dict()
    ignore_fields = tuple(ignore_fields)
    if primary_field is None:
        schema.update({'id': 'INTEGER PRIMARY KEY AUTOINCREMENT'})
    else:
        schema.update({primary_field: f'{python_to_sql_type(rows[0][primary_field])} PRIMARY KEY'})
        ignore_fields += primary_field,

    for row in rows:
        schema.update(map_to_schema(row, ignore_fields=ignore_fields))

    return schema


def map_to_schema(row: Mapping[str, Any], ignore_fields: Collection[str] = tuple()) -> dict:
    """
    Create Table SQL schema from single data mapping.

    Given data mapping is a sample row instance.
    Row instance map entry must have following structure:
        Field_name: Instance_vale_for_field

    :param rows: sequence of data mappings containing row instances for table
    :param ignore_fields: sequence of field names to ignore
    """
    fields = list(row.keys())
    types = [python_to_sql_type(v) for v in row.values()]
    schema = dict()
    for f, t in zip(fields, types):
        if f not in ignore_fields:
            schema.update({f: t})

    return schema


def python_to_sql_type(value) -> str:
    """
    Convert Python type to an SQL type name.

    :param value: sample of value to extract type from it.
    """
    if isinstance(value, str):
        return "TEXT"
    elif isinstance(value, int):
        return "INTEGER"
    elif isinstance(value, float):
        return "REAL"
    elif isinstance(value, bytes):
        return "BLOB"
    elif value is None:
        return "NULL"
    raise TypeError(f"Not supported type {type(value)}")

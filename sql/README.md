# SQL shit
Database, Table and Query wrapper for SQLite with syntax inspired by Numpy.

## Motivation
Also known as "Why am I going to use your shit instead of SQL shit?"

Just compare theese two equal operations:

**SQL shit**
```sql
SELECT 
        Users.name,Cars.model,Vendors.country 
        FROM (((Users INNER JOIN User_Car ON Users.id = User_Car.user_id) INNER JOIN Cars ON Cars.reg = User_Car.car_reg) INNER JOIN Vendors ON Vendors.id = Cars.vendor_id) WHERE (((Vendors.country = "Russia") OR (Vendors.country = "US")));
```

**My sql shit**
```python
(users & user_car & cars & vendors)['name', 'model', 'country'] == ((),(),("Russia", "US"))
# or with equal method-powered syntax:
users.INNER(user_car).INNER(cars).INNER(vendors).SELECT(['name', 'model', 'country']).WHERE_EQ(((),(),("Russia", "US")))
```

## Quick Start
### 1. Find or create your SQLite dababase file
```python
from easy_pytools.sql import DBase

your_base = DBase("tests/sql_test.sql")
```

### 2. Get existing tables names
```python
your_base.tables
```

### 3. Create new table
create table schema
>Let us imagine that there is already Vendors table with primary key 'id'
```python
schema = {
    "id": "integer primary key autoincrement",
    "name": "varchar(20)",
    "vendor_id": "integer",
    "foreign key(vendor_id)":"references Vendors(id)"
}
```
create new table
```python
printers = your_base.new_table("Printers", schema)
```
Now the 'printers' variable references to 'Table' object that provides all the SQL shit for the 'Printers' table of database.

```python
printers
```
```python
Table<Printers of tests/sql_test.sql>
```

### 4. Get existing table from base
```python
vendors = your_base.table("Vendors")
```
Now the 'vendors' variable references to 'Table' object that provides all the SQL shit for the 'Vendors' table of database.
```python
vendors
```
```python
Table<Vendors of tests/sql_test.sql, Real>
```

### 5. Get information about table
```python
printers.fields
```
```python
{
    'Printers.id': Field<0, id, INTEGER of Table<Printers of tests/sql_test.sql, Real>>,
    'Printers.name': Field<1, name, varchar(20) of Table<Printers of tests/sql_test.sql, Real>>,
    'Printers.vendor_id': Field<2, vendor_id, INTEGER of Table<Printers of tests/sql_test.sql, Real>>
}
```
---
```python
printers.foreign_keys
```
```python
{
    'Printers.vendor_id': TableFK<Field<2, vendor_id, INTEGER of Table<Printers of tests/sql_test.sql, Real>> -> Field<0, id, INTEGER of Table<Vendors of tests/sql_test.sql, Real>>>
}
```
---
```python
printers.foreign_tables
```
```python
{
    Table<Vendors of tests/sql_test.sql, Real>
}
```

### 6. Add rows to table
```python
printers << {"name":"Canon L100", "vendor_id": 1}
printers << {"name":"Canon L200", "vendor_id": 1}
# or use instant method call:
printers.INSERT({"name":"Canon L200", "vendor_id": 1})
```
Foreign Key constraints checked as long as Python sqlite3 checks them.

Also, if your table has no Primary Keys with Autoincrement, you can add rows as tuples:
```python
table << (10, "Hello", 20)
```
In that case values order must match fields order of table.

### 7. Select from table
```python
printers[:]()
```
```python
[
    (1, 'Canon L100', 1),
    (2, 'Canon L200', 1)
]
```
---
```python
printers['name']()
# or use instant method call:
printers.SELECT(['name'])()
```
```python
[
    ('Canon L100',)
    ('Canon L200',)
]
```

#### 7.1. Ordering
You can order selected rows by fields with following syntax:
```python
printers[:] / ('name',)
# or with instant method call:
printers[:].ORDERBY(('name',))
```

#### 7.2. Grouping
You can group selected rows by fields with following syntaxL
```python
printers[:] % ('country',)
# or with instant method call:
printers[:].GROUPBY(('country',))
```

### 8. Table compositioning
Any table composition result is 'Table' object with some restrictions.

So you can, f.ex.,  select from table composition just as from real table.
#### Cartesian product
```python
printers_vendors = printers * vendors
# or with instant method call:
printers_vendors = printers.AND(vendors)

printers_vendors
```
```python
Table<Printers_x_Vendors of tests/sql_test.sql, Composition>
```
```python
printers_vendors[:]()
```
```python
[(1, 'Canon L100', 1, 1, 'Tayouta', 'Japan'),
 (1, 'Canon L100', 1, 2, 'Lada', 'Russia'),
 (1, 'Canon L100', 1, 3, 'KAMAZ', 'Russia'),
 (2, 'Canon L200', 1, 1, 'Tayouta', 'Japan'),
 (2, 'Canon L200', 1, 2, 'Lada', 'Russia'),
 (2, 'Canon L200', 1, 3, 'KAMAZ', 'Russia')]
```
#### JOIN tables
Joining tables may be done two ways:
- automatical join on foreign key with cute syntax
- join on any keys equalities with method

**INNER JOIN**
```python
# Foreign key to composite tables will be automatically detected
# Otherwise exception will be thrown:
printers_vendors = printers & vendors
# or use instant method call:
printers_vendors = printers.INNER(vendors)
# ...you can even manually specify keys to join table:
printers_vendors = printers.join(vendors, 'INNER', printers.f_vendor_id, vendors.f_id)

printers_vendors
```
```python
Table<Printers_INNER_Vendors of tests/sql_test.sql, Composition>
```
```python
printers_vendors.fields
```
```python
{'Printers.id': Field<0, id, INTEGER of Table<Printers of tests/sql_test.sql, Real>>,
 'Printers.name': Field<1, name, varchar(20) of Table<Printers of tests/sql_test.sql, Real>>,
 'Printers.vendor_id': Field<2, vendor_id, INTEGER of Table<Printers of tests/sql_test.sql, Real>>,
 'Vendors.id': Field<0, id, INTEGER of Table<Vendors of tests/sql_test.sql, Real>>,
 'Vendors.name': Field<1, name, varchar(20) of Table<Vendors of tests/sql_test.sql, Real>>,
 'Vendors.country': Field<2, country, varchar(20) of Table<Vendors of tests/sql_test.sql, Real>>}
```
```python
printers_vendors[:]()
```

```python
[
    (1, 'Canon L100', 1, 1, 'Tayouta', 'Japan'),
    (2, 'Canon L200', 1, 1, 'Tayouta', 'Japan')
]
```
**LEFT JOIN**
```python
# Foreign key to composite tables will be automatically detected
# Otherwise exception will be thrown:
printers_vendors = vendors - printers
# or use instant method call:
printers_vendors = printers.LEFT(vendors)
# ...or you can manually specify keys to join table:
printers_vendors = vendors.join(printers, 'LEFT', printers.f_id, printers.f_vendor_id)

printers_vendors
```
```python
Table<Printers_LEFT_Vendors of tests/sql_test.sql, Composition>
```
```python
printers_vendors.fields
```
```python
{'Printers.id': Field<0, id, INTEGER of Table<Printers of tests/sql_test.sql, Real>>,
 'Printers.name': Field<1, name, varchar(20) of Table<Printers of tests/sql_test.sql, Real>>,
 'Printers.vendor_id': Field<2, vendor_id, INTEGER of Table<Printers of tests/sql_test.sql, Real>>,
 'Vendors.id': Field<0, id, INTEGER of Table<Vendors of tests/sql_test.sql, Real>>,
 'Vendors.name': Field<1, name, varchar(20) of Table<Vendors of tests/sql_test.sql, Real>>,
 'Vendors.country': Field<2, country, varchar(20) of Table<Vendors of tests/sql_test.sql, Real>>}
```
```python
printers_vendors[:]()
```
```python
[
    (1, 'Canon L100', 1, 1, 'Tayouta', 'Japan'),
    (2, 'Canon L200', 1, 1, 'Tayouta', 'Japan'),
    (None, None, None, 2, 'Lada', 'Russia'),
    (None, None, None, 3, 'KAMAZ', 'Russia')
]
```

**FULL OUTER JOIN**

Is supported by my lib, but not supported by Python sqlite3.
When Python's sqlite3 achieves this support, my lib will work out-of-the-box with that.

```python
printers_vendors = printers ^ vendors
printers_vendors = printers.FULL(vendors)
```

### 9. Field access
You can access fields from tables. It is useful, f.ex, if you want to use **join** method, which requires TableField object as ref, not string field name.

Any field within table can be accessed as TableField reference with that syntax:
```python
table.f_<field_name>
```
F.ex:
```python
printers.f_name
```
```python
Field<1, name, varchar(20) of Table<Printers of tests/sql_test.sql, Real>>
```
If your field name is, f.ex, "f_count", access it this way:
```python
table.f_f_count
```

### 10. Selection coditions
There are two ways to combine and specify selection conditions:

- **AND** combination of conditions is a **list** of conditions;
- **OR** combinations is a **tuple** of conditions;

To limit rows with field value, you have to specify conditions for all fields mentioned in selection.

Empty tuple means no limitation ob field.

There are several condition types:
- Greater -- ">" operator (or WHERE_GT method)
- Equals -- "==" operator (or WHERE_EQ method)
- Lesser -- "<" operator (or WHERE_LT metho)

To limit selection, use one of theese operators with selection on left and limitation on right:
```python
# Selection with 'country' from vendors without limitations:
vendors['country']
# Selection with 'country' and value limitations
vendors['country'] == ("Russia",)
vendors['country'].WHERE_EQ(("Russia",))
# or even such:
vendors.SELECT(['country']).WHERE_EQ(("Russia",))

# Select country, id from vendors where country = "Russia" or id = 2:
vendors['country', 'id'] == ("Russia", 2)
vendors['country', 'id'].WHERE_EQ(("Russia", 2))

# Select country, id from vendors where country = "Russia" and id = 2:
vendors['country', 'id'] == ['Russia', 2]
vendors['country', 'id'].WHERE_EQ(["Russia", 2])

# Select id, country from vendors where country = "Russia" or country = "Japan":
vendors['id', 'country'] == [(), ("Russia","Japan"),]
vendors['id', 'country'].WHERE_EQ([(), ("Russia","Japan"),])

# Select id, country, name from vendors where (country = "Russia" or country = "Japan") or (id = 10)
vendors['id', 'country'] == (10, ("Russia","Japan"),)
vendors['id', 'country'].WHERE_EQ((10, ("Russia","Japan"),))

# Select id, country, name from vendors where (country = "Russia" or country = "Japan") and (id = 10 or id = 20)
vendors['id', 'country'] == [(10, 20), ("Russia","Japan"),]
vendors['id', 'country'].WHERE_EQ([(10, 20), ("Russia","Japan"),])

```

You can also combine different comparisons with AND operator:
```python
# select id, country from vandors where (id = 10 or country = "Japan") AND (id < 20):
(vendors['id'] == (10, "Japan")) < (20,)
# these two are equal to each other and to the previous one
vendors['id'].WHERE_EQ((10, "Japan")).WHERE_LT((20,))
vendors['id'].WHERE_EQ((10, "Japan")).AND.WHERE_LT((20,))
```

To combine different comparisons with OR, use special property:
```python
# select id, country from vandors where (id = 10 or country = "Japan") OR (id < 20):
(vendors['id'] == (10, "Japan")).OR < (20,)
vendors['id'].WHERE_EQ((10, "JAPAN")).OR.WHERE_LT((20,))
```

Note, that every selection is a SelectQuery object. To select values from database, call selection:
```python
vendors[:]
```

```python
SELECT 
        Vendors.id,Vendors.name,Vendors.country 
        FROM Vendors ;
```
---
```python
vendors[:]()
```
```python
[(1, 'Tayouta', 'Japan'), (2, 'Lada', 'Russia'), (3, 'KAMAZ', 'Russia')]
```
---
```python
q = vendors['id', 'name'] > (1,)
# or use a method:
q = vendors['id', 'name'].WHERE_GT((1,))

q
```
```python
SELECT 
        Vendors.id, Vendors.name 
        FROM Vendors WHERE ((Vendors.id > 1));
```
```python
q()
```
```python
[(2, 'Lada'), (3, 'KAMAZ')]
```

### 11. Update values in table

As for now, UPDATE operation is very similar to SELECT: you have to select rows to update and specify fields to update in selected rows.

So, update syntax is very similar to insert syntax, just for SelectQuery instead of Table:
```python
# Update values with tuple. You must specify all values in same order as they are in selection:
(vendors['name'] == ("Tayouta",)) << ("Tamoyo",)
(vendors['name'].WHERE_EQ(("Tayouta",))) << ("Tamoyo",) # etc..

# Wrong assignment type, throws exception:
vendors['id'] == (10,)) << ("Tamoyo",) # Exception
# Wrong assignment shape, throws exception:
vendors['id', 'name'] == ((10, 2),)) << ("Tamoyo",) # Exception
# Gaps are NOT SUPPORTED due to a logical deviation of operation:
vendors['id', 'name'] == ((10, 2),)) << ((), "Tamoyo",) # Excption

# Update values with dict. You can specify any field assignment:
(vendors['id'] == ((2, 3),)) << {"name": "Tamoyo"}
(vendors['id', 'name'] == ((2, 3),)) << {"name": "Tamoyo"}
```

### 12. Aggregate functions
Aggregate functions are available in separate submodule:
```python
from easy_pytools.sql import aggregate as ag
```

Use aggregates instead of regular field names in selection query:
```python
(printers & vendors)[ag.COUNT('Vendors.name')]

# or you can use group by expressions as well:
(printers & vendors)[ag.COUNT('Vendors.name'), 'country'] % ('country',)
(printers & vendors)[ag.COUNT('Vendors.name'), 'country'].GROUPBY(('country',))

```

#### 12.1. Aggregate function selection conditions
Just set conditions like to regular fields, selection object would automatically detect calculated fields and put them to HAVING section of query:
```python
((printers & vendors)[ag.COUNT('Vendors.name'), 'country'] % ('country',)) == [2, ("Japan", "Russia")]
(printers & vendors)[ag.COUNT('Vendors.name'), 'country'].GROUPBY(('country',)).WHERE_EQ([2, ("Japan", "Russia")])
```
```sql
SELECT 
        COUNT(Vendors.name),Vendors.country 
        FROM (Printers INNER JOIN Vendors ON Vendors.id = Printers.vendor_id) WHERE (((Vendors.country = "Japan") OR (Vendors.country = "Russia"))) GROUP BY Vendors.country HAVING ((COUNT(Vendors.name) = 2));

```
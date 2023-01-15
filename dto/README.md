# DataTransferObject class enhancement

## Motivation
DTO pattern is great, but sometimes a bit annoying to implement.

In this part of easy_tools I try to implement some useful autimatizations for building DTO classes.

## Features
- Class fields with metadata and constraints.
- "Data contracts" -- descriptional dictionary with metadata, useful for building auto-generated UI
- Type checking

## Quick Start
import transfer_object decorator and create meta-class with default values:
```python
from easy_pytools.dto import transfer_object

@transfer_object
class Person:
    name = "Noname"
    sex = "M"
    age = 0
```
The value you set is the default value. It is required to extract field type. Do not set 'None' - this is NoneType.

Lets check some information about our class:
```python
p1 = Person()
p1.get_contract()
```
```python
[
    {'field': 'name', 'name': 'name', 'type': <class 'str'>, 'default': 'Noname', 'value': 'Noname', 'allowed': ()},
    {'field': 'sex', 'name': 'sex', 'type': <class 'str'>, 'default': 'M', 'value': 'M', 'allowed': ()},
    {'field': 'age', 'name': 'age', 'type': <class 'int'>, 'default': 0, 'value': 0, 'allowed': ()}]
```
^^ This is a **contract**. Let us explore contract item:
```python
{
    'field': 'name',  # Name of the class instance field
    'name': 'name',  # Associated 'friendly' name for the field
    'type': <class 'str'>,  # Type of data for the field
    'default': 'Noname',  # Default value
    'value': 'Noname',  # Current value
    'allowed': ()  # Tuple of allowed value variants
}
```

You should know smth about fields before we go forward:
- **type** is hard-constrained: you would not be able to set value of other type, but you can set value of child-type
- **allowed** tuple is the hardest constraint: you can set only values, that are in this tuple. If this tuple is empty, any value of specified **type** could be set
- **field** is a _real_ property name as it is in your instance
- **name** is an associated name, useful for, fex, UI or just understanding about _what_ is stored in this instance field

Lets try to violate type constraint:
```python
p1.name = "Vasyan"  # Works good
p1.age = None  # Exception will be thrown:
```
```python
TypeError: <class 'NoneType'> is not a vaild type for age in <class '__main__.Person'> contract. Use <class 'int'>
```
#### How to set values
You can set value two ways:
```python
p1.age = 20
p1.set_value('age', 20)
```

Also if you exactly know order of public fields you can use _write_tuple_ method.

You'll have to pass values for all transfer object fields:
```python
# Throws an exception:
name_sex = ("Vasya", "M")
p1.write_tuple(name_sex)

# Lets do it right way:
name_sex_age = ("Vasya", "M", 19)
p1.write_tuple(name_sex_age)
```

### Playing with field metadata
#### Field associated names
You can associate any name for the field, just give not only default value on class definition, but associative name as well:
```python
@transfer_object
class Person:
    name = "Person's name", "Noname"
    sex = "Person's Sex", "M"
    age = "Person's Age", 0

p1 = Person()
p1.get_contract()
```
```python
[
    {'field': 'name', 'name': "Person's name", 'type': <class 'str'>, 'default': 'Noname', 'value': 'Noname', 'allowed': ()},
    {'field': 'sex', 'name': "Person's Sex", 'type': <class 'str'>, 'default': 'M', 'value': 'M', 'allowed': ()},
    {'field': 'age', 'name': "Person's Age", 'type': <class 'int'>, 'default': 0, 'value': 0, 'allowed': ()}
]
```
As you can see, the first given value -- is field associated name, and the second is default value.
#### Allowed values constraints
Lets specify allowed values for SEX field:
```python
@transfer_object
class Person:
    name = "Person's name", "Noname"
    sex = "Person's Sex", "M", ("M", "F")  # Here you are
    age = "Person's Age", 0

p1 = Person()
p1.get_contract()
```
```python
[
    {'field': 'name', 'name': "Person's name", 'type': <class 'str'>, 'default': 'Noname', 'value': 'Noname', 'allowed': ()},
    {'field': 'sex', 'name': "Person's Sex", 'type': <class 'str'>, 'default': 'M', 'value': 'M', 'allowed': ('M', 'F')},
    {'field': 'age', 'name': "Person's Age", 'type': <class 'int'>, 'default': 0, 'value': 0, 'allowed': ()}
]
```

Now let us try to set different values to sex field:
```python
p1.sex = "M"  # Good
p1.sex = "F"  # Good
p1.sex = 10  # TypeError
p1.sex = "Other"  # Type if OK, but 'Other' is not allowed value, so TypeError:
```
```python
ValueError: 'Other' in not allowed for sex in <class '__main__.Person'> contract. Allowed: ('M', 'F')
```

### Manual metadata setup
You can set metadata manually by including protected attributes:
```python
@transfer_object
class Person:
    name = "Noname"
    _name_contract_name = "Person's name"
    _name_contract_type = str
    sex = "M"
    _sex_contract_name = "Person's sex"
    _sex_contract_type = str
    _sex_contract_allowed = ("M", "F", "Other")
    age = 0
    _age_contract_name = "Person's age"
    _age_contract_type = float
```
As you can see, I am a bit noughty this time: default value for age is Integer, but contract type set to Float.

Let us see, what happens when I try to set Age value:
```python
p1 = Person()
p1.age = 10  # Exception:
```
```python
TypeError: <class 'int'> is not a vaild type for age in <class '__main__.Person'> contract. Use <class 'float'>
```

This is right way:
```python
p1 = Person()
p1.age = 10.0  # Good
```
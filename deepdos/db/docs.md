# deepdos.db.firewall_tiny_db

## TinyFirewall
```python
TinyFirewall(self)
```

Firewall database implementation using tinydb! tinydb is written entirely
in python,allowing a lightweight database system to be utilized by deepdos
without having any external database software installed.

Properties:
    database - The tinydb database instance.
    offenders_table - The tinydb table instance for all registered offenders.
    input_table - The tinydb table instance for all banned input flows.
    output_table - The tinydb table insance for all banned output flows.

### register_tables
```python
TinyFirewall.register_tables(self) -> (<class 'tinydb.database.Table'>, <class 'tinydb.database.Table'>, <class 'tinydb.database.Table'>)
```

Register the tables inside of the TinyDB database

Returns:
    A tuple of all the created/found tables in your database

### insert_offender
```python
TinyFirewall.insert_offender(self, offender: deepdos.firewall.offender.Offender)
```

Insert an offender into the offenders table

### update_offender
```python
TinyFirewall.update_offender(self, offender: deepdos.firewall.offender.Offender)
```

Update an offender in the database

### remove_offender
```python
TinyFirewall.remove_offender(self, offender_connection: str)
```

Remove offenders from the database instance using

### get_offender
```python
TinyFirewall.get_offender(self, offender_connection: str) -> deepdos.firewall.offender.Offender
```

Get an offender given the connection ID

### insert_banned_output
```python
TinyFirewall.insert_banned_output(self, output_data)
```

Insert all banned output flows into the the database after banning them
with the firewall.

### remove_banned_output
```python
TinyFirewall.remove_banned_output(self) -> list
```

Remove all banned output flows from the database.

Returns:
    A list of the output flows to be removed from the firewall

### insert_banned_inputs
```python
TinyFirewall.insert_banned_inputs(self, input_data)
```

Insert all banned input flows into the database after banning them
with the firewall.

### remove_banned_inputs
```python
TinyFirewall.remove_banned_inputs(self) -> list
```

Remove all banned input flows from the database that have expired.

Returns:
    A list of the input flows to be removed from the firewall

# deepdos.db.analytics_tiny_db

Analytics db utilizing tinydb

## TinyAnalytics
```python
TinyAnalytics(self)
```

Analytics database implementation using tinydb! tinydb is written entirely
in python, allowing a lightweight database system to be utilized by deepdos
without having any external database software installed.

Properties:
    database         - The tinydb database instance.
    offenders_table  - The offenders table.
    exceptions_table - The exception table

### register_tables
```python
TinyAnalytics.register_tables(self) -> (<class 'tinydb.database.Table'>, <class 'tinydb.database.Table'>)
```

Register the tables inside of the TinyDB database

Returns:
    A tuple of all the created/found tables in your database

### insert_offender
```python
TinyAnalytics.insert_offender(self, offender: deepdos.firewall.offender.Offender)
```

Insert an offender into the offenders table

### update_offender
```python
TinyAnalytics.update_offender(self, offender: deepdos.firewall.offender.Offender)
```

Update an offender in the database

### insert_exception
```python
TinyAnalytics.insert_exception(self, exception: Exception)
```

Insert the exception into the database.

Args:
    exception - The exception being passed in

# __init__
```python
__init__(*args, **kwargs)
```
Initialize self.  See help(type(self)) for accurate signature.

# deepdos.args.interface

Setting up the interface for listening to data

## obtain_interface_data
```python
obtain_interface_data(desired_interface)
```

Obtain the interface data and return a dictionary that contains
the information of each associated address to that interface

## InterfaceArg
```python
InterfaceArg(self, /, *args, **kwargs)
```

Class for easily command line arguments and their handlers

### register_argument
```python
InterfaceArg.register_argument(self, parser)
```

Register the argument inside of the parser

Args:
    parser - The argument parser object we're registering

### process_argument
```python
InterfaceArg.process_argument(self, args, options: dict)
```

Process the argument into the options

Args:
    args - The namespace object for parsing these
    options - the options dictionary to parse the results into

Returns:
    True if the program is good to go, false if not.

# deepdos.args.argument

The base argument module for all future argument implmementations

## Argument
```python
Argument(self, /, *args, **kwargs)
```

Class for easily command line arguments and their handlers

### register_argument
```python
Argument.register_argument(self, parser)
```

Register the argument inside of the parser

Args:
    parser - The argument parser object we're registering

### process_argument
```python
Argument.process_argument(self, args, options: dict)
```

Process the argument into the options

Args:
    options - the options dictionary to parse the results into

Returns:
    True if the program is good to go, false if not.


# deepdos.args.model

The argument registery

## ModelTypeArg
```python
ModelTypeArg(self, /, *args, **kwargs)
```

Class for easily command line arguments and their handlers

### register_argument
```python
ModelTypeArg.register_argument(self, parser)
```

Register the argument inside of the parser

Args:
    parser - The argument parser object we're registering

### process_argument
```python
ModelTypeArg.process_argument(self, args, options: dict)
```

Process the argument into the options

Args:
    options - the options dictionary to parse the results into

Returns:
    True if the program is good to go, false if not.


# deepdos.args.analytics

The base argument module for all future argument implmementations

## AnalyticsArg
```python
AnalyticsArg(self, /, *args, **kwargs)
```

Class for easily command line arguments and their handlers

### register_argument
```python
AnalyticsArg.register_argument(self, parser)
```

Register the argument inside of the parser

Args:
    parser - The argument parser object we're registering

### process_argument
```python
AnalyticsArg.process_argument(self, args, options: dict)
```

Process the argument into the options

Args:
    options - the options dictionary to parse the results into

Returns:
    True if the program is good to go, false if not.


# deepdos.args.firewall

Picking which firewall type

## FirewallArg
```python
FirewallArg(self, /, *args, **kwargs)
```

Class for easily command line arguments and their handlers

### register_argument
```python
FirewallArg.register_argument(self, parser)
```

Register the argument inside of the parser

Args:
    parser - The argument parser object we're registering

### process_argument
```python
FirewallArg.process_argument(self, args, options: dict)
```

Process the argument into the options

Args:
    options - the options dictionary to parse the results into

Returns:
    True if the program is good to go, false if not.


# deepdos.args.naughty

The naughy count for marking bad flows

## NaughtyCountArg
```python
NaughtyCountArg(self, /, *args, **kwargs)
```

Class for easily command line arguments and their handlers

### register_argument
```python
NaughtyCountArg.register_argument(self, parser)
```

Register the argument inside of the parser

Args:
    parser - The argument parser object we're registering

### process_argument
```python
NaughtyCountArg.process_argument(self, args, options: dict)
```

Process the argument into the options

Args:
    options - the options dictionary to parse the results into

Returns:
    True if the program is good to go, false if not.


# deepdos.args.find_interface

Find all interfaces associated with the current device

## list_interface_data
```python
list_interface_data()
```

List all interface data.

## FindInterfaceArg
```python
FindInterfaceArg(self, /, *args, **kwargs)
```

Class for easily command line arguments and their handlers

### register_argument
```python
FindInterfaceArg.register_argument(self, parser)
```

Register the argument inside of the parser

Args:
    parser - The argument parser object we're registering

### process_argument
```python
FindInterfaceArg.process_argument(self, args, options: dict)
```

Process the argument into the options

Args:
    options - the options dictionary to parse the results into

Returns:
    True if the program is good to go, false if not.


# __init__
```python
__init__(*args, **kwargs)
```
Initialize self.  See help(type(self)) for accurate signature.
# deepdos.args.log

The argument registery

## LogArg
```python
LogArg(self, /, *args, **kwargs)
```

Class for easily command line arguments and their handlers

### register_argument
```python
LogArg.register_argument(self, parser)
```

Register the argument inside of the parser

Args:
    parser - The argument parser object we're registering

### process_argument
```python
LogArg.process_argument(self, args, options: dict)
```

Process the argument into the options

Args:
    options - the options dictionary to parse the results into

Returns:
    True if the program is good to go, false if not.



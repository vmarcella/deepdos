# deepdos.firewall.firewall

Firewall abstraction module

## Firewall
```python
Firewall(self, interface: str, interface_data: dict, naughty_count: int)
```

Firewall class manager for adding rules to our firewall

Args:
    interface - The network interface to write rules for.
    interface_data - The interface data of the interface we're listening to.
    naughty_count - The amount of offenses that we allow a flow to have before.

Properties:
    offenders - A dictionary containing the offending flows.
    input_banned - A dictionary containing the banned input flows.
    output_banned - A dictionary containing the banned output flows.
    ip_version - The IP protocol we're writing rules for.

### create_rule
```python
Firewall.create_rule(self, offender: deepdos.firewall.offender.Offender) -> None
```

Create a firewall rule given the offending connection.

Args:
    offender -> The offending flow that is being banned.


### remove_rule
```python
Firewall.remove_rule(self)
```

Remove rules for the firewall

### track_flows
```python
Firewall.track_flows(self, malicious_flows: list) -> None
```

Track ips that have been marked malicious

Args:
    malicious_flows - List of malicious flow objects to track inside of our firewall

# deepdos.firewall.iptables

Module for linux based firewalls

## IPtable
```python
IPtable(self, interface: str, interface_data: dict, naughty_count: int)
```

Linux based firewall class

Args:
    interface - The network interface we're writing rules for.
    interface_data - A dictionary containing data about the interface.
    naughty_count - The maxmimum amount of offenses a flow can have before being banned.

Properties:
    filter_table - The iptables filter table, where input input and output chains are located.
    input_chain  - The input chain that controls all input rules.
    output_chain - The output chain that controls all output rules.

### create_rule
```python
IPtable.create_rule(self, offender: deepdos.firewall.offender.Offender) -> None
```

Create a firewall rule that will disable communication between the from_ip and
to_ip on the desired interface for the specified protocol.

Args:
    offender - The offending flow to write a rule for.

### remove_rule
```python
IPtable.remove_rule(self)
```

Remove a rule from the table. Still waiting to be written

# __init__
```python
__init__(*args, **kwargs)
```
Initialize self.  See help(type(self)) for accurate signature.
# deepdos.firewall.offender

Lightweight module for keeping track of offenders

## Offender
```python
Offender(self, connection=None, port=None, protocol=None, outbound=None, from_dict=False, doc=None)
```

Offender container for connections that are suspicious

Args:
    src -

### add_offense
```python
Offender.add_offense(self, port, protocol)
```

Add an offense to the offender


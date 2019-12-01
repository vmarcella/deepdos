# deepdos.utils.network

Utility module mainly for executing terminal commands

## log_ip_flow
```python
log_ip_flow(from_ip: str, to_ip: str, prediction: float, proba: float, local_ip: str) -> tuple
```

Log the ip flow information

Args:
    out_info - a Zip object containing:
        from_ip    - pandas series
        to_ip list - pandas series
        prediction - np array of prediction
        proba      - np array of pred probabilities
        local_ip   - The local ip of the interface

Returns:
    Return the output buffer for writing to files

## examine_flow_packets
```python
examine_flow_packets(flow_info: list, local_ip: str) -> tuple
```

Examine and log all flow activity. Will return all malicious packets

Args:
    flow_info - A lists of objects:
        metadata - Dataframe containing meta information
        predictions - NP array containing the predictions for reach row in the metadata
        probas - NP array of the probabilities that each flow is either safe or malicious
    local_ip - The local ip of the interface as a string

Returns:
    A list of all malicious flow objects and another list of the
    flow output buffer containing logs of the malicious flows

## create_firewall
```python
create_firewall(interface: str, interface_data: dict, firewall_type: str, naughty_count: int) -> deepdos.firewall.firewall.Firewall
```

Firewall factory. Will create a firewall based on the type of firewall that is passed in.
Currently, this function only supports linux based operating systems

Args:
    interface - The interface as a string
    interface_data - The interface data as a dictionary
    firewall_type - The name of the firewall to use as a string
    naughty_count - the maximum offenses as an integer

Returns:
    A firewall if successfully setup, None otherwise

# deepdos.utils.flow

## MaliciousFlow
```python
MaliciousFlow(self, ips, ports, protocol)
```

Tracking malicious flows more efficiently with class containers

Properties:
    from_ip - The src ip of the malicious flow
    to_ip   - The destination ip of the malicious flow
    from_port - The port spoken from the src ip
    to_port   - The port spoken to at the destination ip
    protocol  - The protocol that was used for communication
    connection - The Full communication (to and from IP)

# deepdos.utils.processes

Module for spawning subprocesses within deepdos to carry out operations
that this application isn't capable of doing.

## proc_capture_pcap
```python
proc_capture_pcap(interface: str, line_count: int = 5000) -> list
```

Capturing pcap information

Args:
    interface - The desired network interface as a string
    line_count - The amount of lines to be read in by tcpdump
    before aggregating all the packets into flows

Returns:
    the read in bytes as a list

## proc_execute_cicflowmeter
```python
proc_execute_cicflowmeter(etc_dir: str) -> None
```

Execute the cicflowmeter to create the flow csv from the pcap file.

Args:
    etc_dir - The parent directory of all non-code files as a string

## proc_find_deepdos
```python
proc_find_deepdos() -> str
```

Find where deepdos is located in your path

Returns:
    The location of deepdos as a string

## proc_create_linux_symlink
```python
proc_create_linux_symlink(src_location: str) -> None
```

Create a symlink for deepdos so that it can be found on the sudo secure path.

Args:
    src_location: the location where deepdos is installed as a string

Returns:
    Nothing, but will stop the program execution if it couldn't succeed. This is
    because you NEED root privileges in order to utilize network toolings.

# __init__
```python
__init__(*args, **kwargs)
```
Initialize self.  See help(type(self)) for accurate signature.

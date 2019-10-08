"""
    Firewall abstraction module
"""
from abc import ABC, abstractmethod


class Offender:
    """
        Offender container for connections that are suspicious
    """

    def __init__(self, src, port, protocol, outbound):
        self.src = src
        self.offenses = 1
        self.port_mappings = set()
        self.port_mappings.add((port, protocol))
        self.outbound = outbound

    def add_offense(self, port, protocol):
        """
            Add an offense to the offender
        """
        self.offenses += 1
        self.port_mappings.add((port, protocol))

    def __repr__(self):
        return f"src: {self.src} - off: {self.offenses} - port/proto: {self.port_mappings}, out: {self.outbound}"


class Firewall(ABC):
    """
        Firewall class manager for adding rules to our firewall
    """

    def __init__(self, interface: str, interface_data: dict, naughty_count: int):
        # Setup general data
        self.interface = interface
        self.interface_data = interface_data
        self.naughty_count = naughty_count
        self.offenders = {}
        self.input_banned = {}
        self.output_banned = {}
        self.ip_version = "2"

    @abstractmethod
    def create_rule(self, offender: Offender):
        """
            Create a firewall rule given:
                ips - tuple(from_ip, to_ip)
                ports - tuple(from_port, to_port)
                protocol: "TCP"
        """
        return NotImplemented

    @abstractmethod
    def remove_rule(self):
        """
            Remove rules for the firewall
        """
        return NotImplemented

    def track_flows(self, malicious_flows):
        """
            Track ips that have been marked malicious
        """
        print(self.offenders)
        interface_info = self.interface_data[self.ip_version]
        local_ip = interface_info["address"]

        # Iterate through the malicious ips list
        for flow in malicious_flows:

            # Was this connection outbound or inbound?
            outbound = True if flow.from_ip == local_ip else False

            # Which port on are computer are we blocking??
            port = flow.from_port if outbound else flow.to_port
            print(port)

            # Check if the connection occurred
            if flow.connection in self.offenders:
                offender = self.offenders[flow.connection]

                # They've had way too many violations, it's time to ban this malicious data.
                if offender.offenses > self.naughty_count:
                    self.create_rule(offender)
                    del self.offenders[flow.connection]
                else:
                    print(" - Adding an offense to flow:")
                    print(f"\t{flow}")
                    offender.add_offense(port, flow.protocol)

            else:
                # Register the flow as an offender :(
                self.offenders[flow.connection] = Offender(
                    flow.connection, port, flow.protocol, outbound
                )

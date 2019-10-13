"""
    Firewall abstraction module
"""
from abc import ABC, abstractmethod

from deepdos.conf import create_logger
from deepdos.firewall.offender import Offender


class Firewall(ABC):
    """
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
        self.logger = create_logger(__name__, "INFO")

    @abstractmethod
    def create_rule(self, offender: Offender) -> None:
        """
            Create a firewall rule given the offending connection.

            Args:
                offender -> The offending flow that is being banned.

        """
        return NotImplemented

    @abstractmethod
    def remove_rule(self):
        """
            Remove rules for the firewall
        """
        return NotImplemented

    def track_flows(self, malicious_flows: list) -> None:
        """
            Track ips that have been marked malicious

            Args:
                malicious_flows - List of malicious flow objects to track inside of our firewall
        """
        interface_info = self.interface_data[self.ip_version]
        local_ip = interface_info["address"]

        # Iterate through the malicious ips list
        for flow in malicious_flows:

            # Was this connection outbound or inbound?
            outbound = True if flow.from_ip == local_ip else False

            # Which port on are computer are we blocking??
            port = flow.from_port if outbound else flow.to_port

            # Check if the connection occurred
            if flow.connection in self.offenders:
                offender = self.offenders[flow.connection]

                # They've had way too many violations, it's time to ban this malicious data.
                if offender.offenses > self.naughty_count:
                    self.create_rule(offender)
                    del self.offenders[flow.connection]
                else:
                    self.logger.info(f"Adding an offense to flow: {flow.connection}")
                    offender.add_offense(port, flow.protocol)
                    self.logger.info(f"Flow: {flow} Offenses: {offender.offenses}")

            else:
                self.logger.info(f"First offense for flow: {flow.connection}")
                # Register the flow as an offender :(
                self.offenders[flow.connection] = Offender(
                    flow.connection, port, flow.protocol, outbound
                )

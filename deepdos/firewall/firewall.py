"""
    Firewall abstraction module
"""
from abc import ABC, abstractmethod

from colorama import Fore
from deepdos.conf import create_logger
from deepdos.db.firewall_tiny_db import TinyFirewall
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
        self.database = TinyFirewall()
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
            offender: Offender = self.database.get_offender(flow.connection)

            if offender:
                # They've had way too many violations, it's time to ban this malicious data.
                if offender.offenses > self.naughty_count:
                    self.create_rule(offender)
                    self.database.remove_offender(offender.connection)
                else:

                    self.logger.info(
                        f"Adding an offense to flow: {Fore.MAGENTA}{flow.connection}{Fore.WHITE}"
                    )
                    offender.add_offense(port, flow.protocol)
                    self.database.update_offender(offender)
                    self.logger.info(
                        f"Flow: {Fore.MAGENTA}{flow}{Fore.WHITE} Offenses: {Fore.RED}{offender.offenses}{Fore.WHITE}"
                    )

            else:
                self.logger.info(
                    f"First offense for flow: {Fore.MAGENTA}{flow.connection}{Fore.WHITE}"
                )
                # Register the flow as an offender :(
                self.database.insert_offender(
                    Offender(flow.connection, port, flow.protocol, outbound)
                )

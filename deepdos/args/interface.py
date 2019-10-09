"""
    Setting up the interface for listening to data
"""
import psutil
from deepdos.args.argument import Argument


def obtain_interface_data(desired_interface):
    """
        Obtain the interface data and return a dictionary that contains
        the information of each associated address to that interface
    """
    addrs = psutil.net_if_addrs()
    data = {}

    # Check if the desired interface is valid
    if desired_interface in addrs:
        nic = addrs[desired_interface]
        # Store all associated addresses for managing our firewall
        for info in nic:
            # add data for the current address family
            data[f"{info.family}"] = {
                "address": str(info.address),
                "netmask": str(info.netmask),
                "broadcast": str(info.broadcast),
                "ptp": str(info.ptp),
            }
        return data

    # Couldn't find the requested interface
    raise ValueError(f"Couldn't find the requested interface: {desired_interface}")


class InterfaceArg(Argument):
    """
        Class for easily command line arguments and their handlers
    """

    def register_argument(self, parser):
        """
            Register the argument inside of the parser

            Args:
                parser - The argument parser object we're registering
        """
        # Read in the interface
        parser.add_argument(
            "-i",
            action="store",
            dest="interface",
            help="[REQUIRES SUDO] The network interface for deepdos to listen to",
            default=None,
        )

    def process_argument(self, args, options: dict):
        """
            Process the argument into the options

            Args:
                args - The namespace object for parsing these 
                options - the options dictionary to parse the results into

            Returns:
                True if the program is good to go, false if not.
        """
        # Store the interface and interface data
        if args.interface:
            options["interface"] = args.interface
            options["interface_data"] = obtain_interface_data(args.interface)
            return True
        else:
            return False

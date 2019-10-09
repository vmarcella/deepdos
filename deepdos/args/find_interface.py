"""
    Find all interfaces associated with the current device
"""
import psutil
from deepdos.args.argument import Argument


def list_interface_data():
    """
        List all interface data.
    """
    addrs = psutil.net_if_addrs()
    for address, nic in addrs.items():
        print(f"interface: {address}")
        # Iterate through each associated address and it's information
        for info in nic:
            print("\tAssociated address:")
            print(f"\t\tFamily: {info.family}")
            print(f"\t\tAddress: {info.address}")
            print(f"\t\tNetmask: {info.netmask}")
            print(f"\t\tBroadcast: {info.broadcast}")
            print(f"\t\tPTP: {info.ptp}")
        print()

    print(
        "Pick one of these interfaces to listen to traffic on, and then rerun the command with it :)"
    )
    exit()


class FindInterfaceArg(Argument):
    """
        Class for easily command line arguments and their handlers
    """

    def register_argument(self, parser):
        """
            Register the argument inside of the parser

            Args:
                parser - The argument parser object we're registering
        """
        # Find all user interfaces
        parser.add_argument(
            "--find-interface",
            action="store_true",
            dest="find_interface",
            help="List all of your devices network interfaces. Good if you don't know what interfaces your device has",
            default=False,
        )

    def process_argument(self, args, options: dict):
        """
            Process the argument into the options

            Args:
                options - the options dictionary to parse the results into

            Returns:
                True if the program is good to go, false if not.

        """
        # Find all interfaces if specified and then exit
        if args.find_interface:
            # List all of the interface data
            print(args)
            list_interface_data()

        return True

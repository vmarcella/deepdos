import argparse

import psutil


def create_parser():
    """
        Create the argument parser with some default arguments

        Returns:
            The arguments
    """
    parser = argparse.ArgumentParser(
        description="Welcome to deepdos, the machine learning/ai based ddos analysis/mitigation service"
    )
    # Read in the interface
    parser.add_argument(
        "-i",
        action="store",
        dest="interface",
        help="the network interface for deepdos to listen to",
        default=None,
    )

    parser.add_argument(
        "--find-interface", action="store_true", dest="find_interface", default=False
    )

    return parser.parse_args()


def parse_args():
    """
        Parse the arguments of the arg parser
        Return the options that will be used to configure the main loop
    """
    args = create_parser()
    options = {}

    # Find all interfaces if specified and then exit
    if args.find_interface:
        addrs = psutil.net_if_addrs()
        for address, nic in addrs.items():
            print(f"interface: {address}")
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

    # Use the passed in interface or exit app
    if args.interface:
        options["interface"] = args.interface
        print(args.interface)
    else:
        print(
            "You need to provide a network interface for deepdos to listen on, or run --find-interface to list all of them."
        )
        exit()

    return options

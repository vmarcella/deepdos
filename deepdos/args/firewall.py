"""
    Picking which firewall type
"""
from deepdos.args.argument import Argument


class FirewallArg(Argument):
    """
        Class for easily command line arguments and their handlers
    """

    def register_argument(self, parser):
        """
            Register the argument inside of the parser

            Args:
                parser - The argument parser object we're registering
        """
        # Activate firewall mode with a specified firewall
        parser.add_argument(
            "--firewall",
            action="store",
            help="[REQUIRES SUDO] Turn on firewall mode for the given system. linux for Linux systems and macos for mac (Not yet supported)",
            dest="firewall",
            default=None,
        )

    def process_argument(self, args, options: dict):
        """
            Process the argument into the options

            Args:
                options - the options dictionary to parse the results into

            Returns:
                True if the program is good to go, false if not.

        """
        # Check if firewall is set and set to a valid system
        if args.firewall and args.firewall.lower() in ("linux", "macos"):
            options["firewall"] = args.firewall.lower()
        else:
            options["firewall"] = None

        return True

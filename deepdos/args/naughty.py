"""
    The naughy count for marking bad flows
"""
from deepdos.args.argument import Argument


class NaughtyCountArg(Argument):
    """
        Class for easily command line arguments and their handlers
    """

    def register_argument(self, parser):
        """
            Register the argument inside of the parser

            Args:
                parser - The argument parser object we're registering
        """
        # Read in the naughty count
        parser.add_argument(
            "-n",
            action="store",
            dest="naughty_count",
            type=int,
            help="The amount of malicious flows that can come from a given address",
            default=10,
        )

    def process_argument(self, args, options: dict):
        """
            Process the argument into the options

            Args:
                options - the options dictionary to parse the results into

            Returns:
                True if the program is good to go, false if not.

        """

        options["naughty_count"] = args.naughty_count
        return True

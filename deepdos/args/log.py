"""
    The argument registery
"""
from deepdos.args.argument import Argument


class LogArg(Argument):
    """
        Class for easily command line arguments and their handlers
    """

    def register_argument(self, parser):
        """
            Register the argument inside of the parser

            Args:
                parser - The argument parser object we're registering
        """
        parser.add_argument(
            "--log",
            action="store",
            help="Set the log level. Can choose from: [DEBUG, INFO, WARNING, ERROR, CRITICAL]",
            dest="log",
            default="INFO",
        )

    def process_argument(self, args, options: dict):
        """
            Process the argument into the options

            Args:
                options - the options dictionary to parse the results into

            Returns:
                True if the program is good to go, false if not.

        """
        options["log"] = args.log
        return True

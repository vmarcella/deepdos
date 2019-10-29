"""
    The base argument module for all future argument implmementations
"""
from deepdos.analytics import AnalyticsEngine
from deepdos.args.argument import Argument


class AnalyticsArg(Argument):
    """
        Class for easily command line arguments and their handlers
    """

    def register_argument(self, parser):
        """
            Register the argument inside of the parser

            Args:
                parser - The argument parser object we're registering
        """
        # Register the user for analytics
        parser.add_argument(
            "--find-interface",
            action="store_true",
            dest="analytics",
            help="Enable analytics to be stored with your consent. Otherwise, no analytics are stored and sent off.",
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
        if args.analytics:
            options["analytics"] = AnalyticsEngine()
        else:
            options["analytics"] = None

        return True

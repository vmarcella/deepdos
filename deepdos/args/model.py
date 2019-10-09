"""
    The argument registery
"""
from deepdos.args.argument import Argument
from deepdos.conf import LATEST_STABLE_MODEL


class ModelTypeArg(Argument):
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
            "--model-type",
            action="store",
            help="The model that you would like to use for classifying the data",
            dest="model_type",
            default=f"{LATEST_STABLE_MODEL}",
        )

    def process_argument(self, args, options: dict):
        """
            Process the argument into the options

            Args:
                options - the options dictionary to parse the results into

            Returns:
                True if the program is good to go, false if not.

        """
        options["model_type"] = args.model_type
        return True

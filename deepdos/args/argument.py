"""
    The base argument module for all future argument implmementations
"""
from abc import ABC, abstractmethod


class Argument(ABC):
    """
        Class for easily command line arguments and their handlers
    """

    @abstractmethod
    def register_argument(self, parser):
        """
            Register the argument inside of the parser

            Args:
                parser - The argument parser object we're registering
        """

        raise NotImplementedError()

    @abstractmethod
    def process_argument(self, args, options: dict):
        """
            Process the argument into the options

            Args:
                options - the options dictionary to parse the results into

            Returns:
                True if the program is good to go, false if not.

        """

        raise NotImplementedError()

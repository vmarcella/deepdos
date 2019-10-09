"""
    The argument registry
"""
import argparse
from abc import ABC, abstractmethod

from deepdos.args.find_interface import FindInterfaceArg
from deepdos.args.firewall import FirewallArg
from deepdos.args.interface import InterfaceArg
from deepdos.args.log import LogArg
from deepdos.args.model import ModelTypeArg
from deepdos.args.naughty import NaughtyCountArg


def create_parser(argument_objects):
    """
        Create the argument parser with some default arguments

        Returns:
            The arguments
    """
    # Create the arg parser
    parser = argparse.ArgumentParser(
        description="Welcome to deepdos, the machine learning/ai based ddos analysis/mitigation service",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    for obj in argument_objects:
        obj.register_argument(parser)

    return parser


def parse_args():
    """
        Parse the arguments of the arg parser
        Return the options that will be used to configure the main loop
    """
    # Argument objects
    argument_objects = [
        FindInterfaceArg(),
        InterfaceArg(),
        NaughtyCountArg(),
        FirewallArg(),
        ModelTypeArg(),
        LogArg(),
    ]

    # Create the parser and parse the args
    parser = create_parser(argument_objects)
    parsed_args = parser.parse_args()
    options = {}

    # Parse all of the options
    for obj in argument_objects:
        if not obj.process_argument(parsed_args, options):
            parser.print_usage()
            exit()

    return options

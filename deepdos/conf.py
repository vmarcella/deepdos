"""
    Global variables
"""
import logging
import os
import sys

from deepdos.utils.processes import (proc_create_linux_symlink,
                                     proc_find_deepdos)

# Get the root directory for deepdos
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Directory for dependencies, models, logs and anything else
# that isn't code related
ETC_DIR = f"{ROOT_DIR}/.etc"

# Latest stable model
LATEST_STABLE_MODEL = "lr-stable-0.9.0.pickle"


def create_logger(module_name: str, log_level: str) -> logging.Logger:
    """
        Create a logger object based on the pythons module name

        Args:
            module_name - The name of the module to create the logger for as.
            log_level   - The log level to be logging output at.

        Returns:
            A customized logger object for deepdos logging
    """
    logger = logging.getLogger(module_name)
    logger.setLevel(log_level)

    channel = logging.StreamHandler()
    channel.setLevel(log_level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    channel.setFormatter(formatter)

    logger.addHandler(channel)
    return logger


def create_etc_dirs():
    """
        Create all directories needed for deepdos to properly execute. Only
        runs if the logs directory isn't created.
    """
    # Load in the folders that don't exist
    folders = ["logs", "pcap_info", "flow_output", "db"]

    for folder in folders:
        if not os.path.exists(f"{ETC_DIR}/{folder}"):
            os.mkdir(f"{ROOT_DIR}/.etc/{folder}")


def setup_root_access():
    """
        Setup root access for the deepdos command line utility.
        This is needed so that there is tcpdump and iptable access
    """
    if not os.path.exists(f"{ETC_DIR}/.haslink") and os.geteuid() != 0:

        if sys.platform == "linux":
            location = proc_find_deepdos()
            proc_create_linux_symlink(location)
            open(f"{ETC_DIR}/.haslink", "w+").close()
            print("You can now rerun deepdos as root user!")
            exit()

        else:
            # User is signed into non-linux
            print("You need to be root in order to run these commands!")
            exit(1)


def load_conf():
    """
        Ensure all config is loaded before the program is set.
    """
    create_etc_dirs()
    setup_root_access()

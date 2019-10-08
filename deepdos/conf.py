"""
    Global variables
"""
import getpass
import os
import subprocess
import sys

# Get the root directory for deepdos
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Directory for dependencies, models, logs and anything else
# that isn't code related
ETC_DIR = f"{ROOT_DIR}/.etc"

# Latest stable model
LATEST_STABLE_MODEL = "lr-stable-0.9.0.pickle"


def create_etc_dirs():
    """
        Create etc logging directories for all subprocesses
        to function properly
    """
    # Load in the folders that don't exist
    if not os.path.exists(f"{ETC_DIR}/logs"):
        folders = ["logs", "pcap_info", "flow_output"]
        for folder in folders:
            os.mkdir(f"{ROOT_DIR}/.etc/{folder}")


def setup_root_access():
    """
        Setup root access for the deepdos command line utility.
        This is needed so that there is tcpdump and iptable access
    """
    if not os.path.exists(f"{ETC_DIR}/.haslink") and os.geteuid() != 0:

        # Obtain the deepdos bin location post install
        get_deepdos = ["which", "deepdos"]
        process = subprocess.Popen(get_deepdos, stdout=subprocess.PIPE)
        location = process.stdout.readline()
        process.stdout.close()
        exit_status = process.wait()

        if exit_status or not location:
            print("You didn't properly install deepdos :/")
            exit(1)

        if sys.platform == "linux":
            user_input = input(
                "deepdos can setup a symlink inside of /usr/bin/deepdos for you if you'd\n"
                "like to be able to easily access deepdos via sudo. If you can already access\n"
                "deepdos with sudo, then you can just say exit or press N.\n"
                "Would you like deepdos to try and create a symlink? [y/N]"
            )

            if user_input != "y":
                print("Shutting down. Cannot access network utilities without sudo.")
                exit()

            # Create link command
            create_link = [
                "sudo",
                "ln",
                "-s",
                location.decode("utf-8").rstrip(),
                "/usr/bin/deepdos",
            ]

            # Spawn the create_link subprocess
            process = subprocess.Popen(
                create_link,
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            print(
                "For initial setup, deepdos needs your password to create a symlink @ /usr/bin/deepdos\n"
                "to ensure that your sudo user has it! You can enter your password down below if prompted."
            )

            # Get the first
            _, std_err = process.communicate(input="")

            # Obtain the sudo password from the user
            while std_err.decode("utf-8") == f"[sudo] password for {getpass.getuser()}":
                sudo_password = str(getpass.getpass(prompt=std_err.decode("utf-8")))
                _, std_err = process.communicate(input=sudo_password)

            exit_status = process.wait()

            # Couldn't authenticate successfully
            if exit_status:
                print(std_err.decode("utf-8").rstrip())
                exit(1)

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

"""
    Global variables
"""
import getpass
import os
import subprocess

# Get the root directory for deepdos
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Latest stable model
LATEST_STABLE_MODEL = "lr-stable-0.9.0.pickle"


def create_etc_dirs():
    """
        Create etc logging directories for all subprocesses
        to function properly
    """
    # Load in the folders that don't exist
    if not os.path.exists(f"{ROOT_DIR}/logs"):
        folders = ["logs", "pcap_info", "flow_output"]
        for folder in folders:
            os.mkdir(f"{ROOT_DIR}/{folder}")


def setup_root_access():
    """
        Setup root access for the deepdos command line utility.
        This is needed so that there is tcpdump and iptable access
    """
    if not os.path.exists(f"{ROOT_DIR}/.haslink") and os.getuid() != 0:

        # Obtain the deepdos bin location post install
        get_deepdos = ["which", "deepdos"]
        process = subprocess.Popen(get_deepdos, stdout=subprocess.PIPE)
        location = process.stdout.readline()
        process.stdout.close()
        exit_status = process.wait()

        if exit_status or not location:
            print("You didn't properly install deepdos :/")
            exit(1)

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
            "Hi, I see it's your first time running deepdos!\n"
            "For initial setup, deepdos needs your password to create a symlink @ /usr/bin/deepdos\n"
            "to ensure that your sudo user has it! You can enter your password down below."
        )
        _, std_err = process.communicate(input="")
        while std_err.decode("utf-8") == f"[sudo] password for {getpass.getuser()}":
            sudo_password = str(getpass.getpass(prompt=std_err.decode("utf-8")))
            _, std_err = process.communicate(input=sudo_password)

        exit_status = process.wait()

        if exit_status:
            # Log the error that had occurred
            print(std_err.decode("utf-8").rstrip())
            exit()

        open(f"{ROOT_DIR}/.haslink", "w+").close()
        print("You can now rerun deepdos as root user!")
        exit(1)


def load_conf():
    """
        Ensure all config is loaded before the program is set.
    """
    create_etc_dirs()
    setup_root_access()

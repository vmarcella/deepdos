"""
    Module for spawning subprocesses within deepdos to carry out operations 
    that this application isn't capable of doing.
"""
import getpass
import subprocess


def proc_capture_pcap(interface: str, line_count: int = 5000) -> list:
    """
        Capturing pcap information

        Args:
            interface - The desired network interface as a string
            line_count - The amount of lines to be read in by tcpdump
            before aggregating all the packets into flows

        Returns:
            the read in bytes as a list
    """
    # pcap command with tcpdump (supported by both macos and )
    pcap_cmd = ["tcpdump", "-i", interface, "-s", "65535", "-w", "-"]

    # Spawn the pcap process
    process = subprocess.Popen(
        pcap_cmd,
        stdout=subprocess.PIPE,
        universal_newlines=False,
        encoding="ISO-8859-1",
    )

    counter = 0
    output_list = []

    # Accrue packets for as long as the line count is.
    # made to be customizable
    while counter < line_count:
        line = process.stdout.readline()
        output_list.append(line)
        counter += 1

    # Close the std output file stream
    process.stdout.close()

    # Wait for the process to be killed
    exit_status = process.wait()

    # If the exit wasn't graceful, throw an error
    if exit_status:
        raise subprocess.CalledProcessError(exit_status, pcap_cmd)

    return output_list


def proc_execute_cicflowmeter(etc_dir: str) -> None:
    """
        Execute the cicflowmeter to create the flow csv from the pcap file.

        Args:
            etc_dir - The parent directory of all non-code files as a string
    """
    # cic flowmeter command that retrieves all .pcap files from pcap_info and creates
    # a flow output for each .pcap file
    cic_cmd = ["sh", "cfm", f"{etc_dir}/pcap_info", f"{etc_dir}/flow_output"]

    # Open up the cic flowmeter
    process = subprocess.Popen(
        cic_cmd,
        cwd=f"{etc_dir}/external/CICFlowMeter-4.0/bin",
        stdout=subprocess.DEVNULL,
    )

    # Wait for the process to be killed
    exit_status = process.wait()

    # If the exit wasn't graceful, throw an error
    if exit_status:
        raise subprocess.CalledProcessError(exit_status, cic_cmd)


def proc_find_deepdos() -> str:
    """
        Find where deepdos is located in your path

        Returns:
            The location of deepdos as a string
    """
    # Obtain the deepdos bin location post install
    get_deepdos = ["which", "deepdos"]

    # Spawn new process
    process = subprocess.Popen(get_deepdos, stdout=subprocess.PIPE)
    location = process.stdout.readline()
    process.stdout.close()
    exit_status = process.wait()

    if exit_status or not location:
        print(
            "deepdos couldn't be found on your path. Please try adding deepdos to your path"
            "or executing it as sudo."
        )
        exit()

    return location.decode("utf-8").rstrip()


def proc_create_linux_symlink(src_location: str) -> None:
    """
        Create a symlink for deepdos so that it can be found on the sudo secure path.

        Args:
            src_location: the location where deepdos is installed as a string

        Returns:
            Nothing, but will stop the program execution if it couldn't succeed. This is
            because you NEED root privileges in order to utilize network toolings.
    """
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
    create_link = ["sudo", "ln", "-s", src_location, "/usr/bin/deepdos"]

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

    # Get cmd output
    _, std_err = process.communicate()

    # Obtain the sudo password from the user
    while std_err.decode("utf-8") == f"[sudo] password for {getpass.getuser()}":
        sudo_password = str(getpass.getpass(prompt=std_err.decode("utf-8")))
        _, std_err = process.communicate(input=sudo_password)

    exit_status = process.wait()

    # Couldn't authenticate successfully, display error
    if exit_status:
        print(std_err.decode("utf-8").rstrip())
        exit()

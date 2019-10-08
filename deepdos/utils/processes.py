"""
    Module for spawning subprocesses within deepdos to carry out operations 
    that this application isn't capable of doing.
"""
import subprocess

from deepdos.conf import ETC_DIR, ROOT_DIR


def proc_capture_pcap(interface, line_count=1000):
    """
        Capturing pcap information
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


def proc_execute_cicflowmeter():
    """
        Execute the cicflowmeter to create the flow csv from the pcap file.
    """
    # cic flowmeter command that retrieves all .pcap files from pcap_info and creates
    # a flow output for each .pcap file
    cic_cmd = ["sh", "cfm", f"{ETC_DIR}/pcap_info", f"{ETC_DIR}/flow_output"]

    # Open up the cic flowmeter
    process = subprocess.Popen(
        cic_cmd,
        cwd=f"{ETC_DIR}/external/CICFlowMeter-4.0/bin",
        stdout=subprocess.DEVNULL,
    )

    # Wait for the process to be killed
    exit_status = process.wait()

    # If the exit wasn't graceful, throw an error
    if exit_status:
        raise subprocess.CalledProcessError(exit_status, cic_cmd)

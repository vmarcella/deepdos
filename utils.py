import subprocess


def capture_pcap(interface: str = "eth0"):
    """
        Capturing pcap information
    """
    pcap_cmd = ["tcpdump", "-i", interface, "-s", "65535", "-w", "-"]

    # Spawn the pcap process
    process = subprocess.Popen(
        pcap_cmd, stdout=subprocess.PIPE, universal_newlines=True, encoding="ISO-8859-1"
    )

    for line in iter(process.stdout.readline, ""):
        yield line

    # Close the std output file stream
    process.stdout.close()

    # Wait for the process to be killed
    exit_status = process.wait()

    # If the exit wasn't graceful, throw an error
    if exit_status:
        raise subprocess.CalledProcessError(exit_status, pcap_cmd)


def main_loop():
    for pcap in capture_pcap("enp3s0"):
        print("-----------START-----------")
        print(pcap)
        print("-----------END-----------")

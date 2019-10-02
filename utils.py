import os
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


def execute_cicflowmeter():
    cic_cmd = ["sh", "bin/CICFlowMeter-4.0/bin/cfm", "pcap_info", "flow_output"]
    process = subprocess.Popen(cic_cmd)


def main_loop():
    counter = 0
    pcap_list = []
    pcap_file = open("pcap_info/out.pcap", "w+", encoding="ISO-8859-1")
    for pcap in capture_pcap("enp3s0"):
        pcap_list.append(pcap)
        counter += 1

        if counter == 1000:
            pcap_file.writelines(pcap_list)
            pcap_file.close()

            execute_cicflowmeter()
            print("wrote output")

            counter = 0
            exit()


main_loop()

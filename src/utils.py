import subprocess

from conf import ROOT_DIR


def log_ip_flow(from_ip, to_ip, prediction, proba):
    """
        Log the ip flow information

        Args:
            out_info - a Zip object containing:
                from_ip    - pandas series
                to_ip list - pandas series
                prediction - np array of prediction
                proba      - np array of pred probabilities

        Returns:
            Return the output buffer for writing to files
    """
    src = f"Src IP: {from_ip}"
    dst = f"Dst IP: {to_ip}"
    pred = f"Prediction: {'Malicious' if prediction else 'Safe'}"
    prob = f"Probabilities:"
    safe = f" - Safe - {proba[0] * 100:.2f}%"
    mal = f" - Malicious - {proba[1]*100:.2f}%"

    # Monolithoc print statement
    print("---IP---")
    print(src)
    print(dst)
    print(pred)
    print(prob)
    print(safe)
    print(mal)
    print("--------")

    return ("---IP BLOCK---", src, dst, pred, prob, safe, mal, "--------")


class MaliciousFlow:
    """
        Tracking malicious flows more efficiently with class containers
    """

    def __init__(self, ips, ports, protocol):
        self.from_ip, self.to_ip = ips
        self.from_port, self.to_port = ports
        self.protocol = protocol
        self.connection = f"{self.from_ip}/{self.to_ip}"

    def __repr__(self):
        return f"{self.from_ip}/{self.to_ip}-{self.from_port}:{self.to_port}-{self.protocol}"


def examine_flow_packets(flow_info):
    """
        Examine and log all flow activity. Will return all malicious packets
    """
    metadata, predictions, probas = flow_info
    malicious_flows = []
    flow_buffer = []
    print(metadata)

    # Iterate through all of the flow information
    for row, prediction, proba in zip(metadata.values, predictions, probas):
        from_ip, to_ip, proto, from_port, to_port = row
        buffer = log_ip_flow(from_ip, to_ip, prediction, proba)
        flow_buffer.append(buffer)

        # If this is classified as malicious, let's report this incident.
        if prediction:
            # Track a new malicious flow
            malicious_flows.append(
                MaliciousFlow((from_ip, to_ip), (from_port, to_port), proto)
            )

    return malicious_flows, flow_buffer


def capture_pcap(interface, line_count=1000):
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


def execute_cicflowmeter():
    """
        Execute the cicflowmeter to create the flow csv from the pcap file.
    """
    # cic flowmeter command that retrieves all .pcap files from pcap_info and creates
    # a flow output for each .pcap file
    cic_cmd = ["sh", "cfm", f"{ROOT_DIR}/pcap_info", f"{ROOT_DIR}/flow_output"]

    # Open up the cic flowmeter
    process = subprocess.Popen(
        cic_cmd, cwd=f"{ROOT_DIR}/bin/CICFlowMeter-4.0/bin", stdout=subprocess.DEVNULL
    )

    # Wait for the process to be killed
    exit_status = process.wait()

    # If the exit wasn't graceful, throw an error
    if exit_status:
        raise subprocess.CalledProcessError(exit_status, cic_cmd)

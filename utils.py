import subprocess


def log_ip_flow(out_info: zip):
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
    out_buffer = []
    for from_ip, to_ip, prediction, proba in out_info:
        src = f"Src IP: {from_ip}"
        dst = f"Dst IP: {to_ip}"
        pred = f"Prediction: {'Malicious' if prediction else 'Safe'}"
        prob = f"Probabilities:"
        safe = f" - Safe - {proba[0] * 100:.2f}%"
        mal = f" - Malicious - {proba[1]*100:.2f}%"

        out_buffer.append(
            ["---IP BLOCK---", src, dst, pred, prob, safe, mal, "--------"]
        )

        # Monolithoc print statement
        print("---IP---")
        print(src)
        print(dst)
        print(pred)
        print(prob)
        print(safe)
        print(mal)
        print("--------")

    return out_buffer


def capture_pcap(interface: str = "eth0", line_count=1000):
    """
        Capturing pcap information
    """
    # pcap command with tcpdump
    # TODO Enable multiple os commands (Will have to determine the OS)
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
    cic_cmd = ["sh", "cfm", "../../../pcap_info", f"../../../flow_output"]

    # Open up the cic flowmeter
    process = subprocess.Popen(
        cic_cmd, cwd="bin/CICFlowMeter-4.0/bin", stdout=subprocess.DEVNULL
    )

    # Wait for the process to be killed
    exit_status = process.wait()

    # If the exit wasn't graceful, throw an error
    if exit_status:
        raise subprocess.CalledProcessError(exit_status, cic_cmd)

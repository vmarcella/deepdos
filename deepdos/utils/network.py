"""
    Utility module mainly for executing terminal commands
"""


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


def create_firewall(
    interface: str, interface_data: dict, firewall_type: str, naughty_count: int
):
    """
            Firewall factory. Will create a firewall based on the type of firewall that is passed in.
            Currently, this function only supports linux based operating systems
        """
    # Check the firewall type
    if firewall_type == "linux":
        from deepdos.firewall.iptables import IPtable, IPTCError

        try:
            return IPtable(interface, interface_data, naughty_count)
        except IPTCError:
            print("Need to be root in order to access firewall")
            return None

    # Invalid firewall

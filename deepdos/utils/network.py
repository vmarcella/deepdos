"""
    Utility module mainly for executing terminal commands
"""
from colorama import Fore, Style
from deepdos.conf import create_logger
from deepdos.firewall.firewall import Firewall
from deepdos.utils.flow import MaliciousFlow

LOGGER = create_logger(__name__, "INFO")


def log_ip_flow(
    from_ip: str, to_ip: str, prediction: float, proba: float, local_ip: str
) -> tuple:
    """
        Log the ip flow information

        Args:
            out_info - a Zip object containing:
                from_ip    - pandas series
                to_ip list - pandas series
                prediction - np array of prediction
                proba      - np array of pred probabilities
                local_ip   - The local ip of the interface

        Returns:
            Return the output buffer for writing to files
    """

    from_ip = (
        f"{Fore.CYAN}{from_ip}{Fore.WHITE}"
        if from_ip == local_ip
        else f"{Fore.MAGENTA}{from_ip}{Fore.WHITE}"
    )
    to_ip = (
        f"{Fore.CYAN}{to_ip}{Fore.WHITE}"
        if to_ip == local_ip
        else f"{Fore.MAGENTA}{to_ip}{Fore.WHITE}"
    )
    pred = (
        f"{Fore.RED}Malicious{Fore.WHITE}"
        if prediction
        else f"{Fore.GREEN}Safe{Fore.WHITE}"
    )
    prob = f"Probabilities:"
    safe = f"{proba[0] * 100:.2f}%"
    mal = f"{proba[1]*100:.2f}%"

    confidence = mal if prediction else safe

    LOGGER.info(
        f"{from_ip} to {to_ip} was classified as {pred} with {Fore.YELLOW}{confidence}{Fore.WHITE} confidence"
    )

    return ("---IP BLOCK---", from_ip, to_ip, pred, prob, safe, mal, "--------")


def examine_flow_packets(flow_info: list, local_ip: str) -> tuple:
    """
        Examine and log all flow activity. Will return all malicious packets

        Args:
            flow_info - A lists of objects:
                metadata - Dataframe containing meta information
                predictions - NP array containing the predictions for reach row in the metadata
                probas - NP array of the probabilities that each flow is either safe or malicious
            local_ip - The local ip of the interface as a string

        Returns:
            A list of all malicious flow objects and another list of the
            flow output buffer containing logs of the malicious flows
    """
    metadata, predictions, probas = flow_info
    malicious_flows = []
    flow_buffer = []

    # Iterate through all of the flow information
    for row, prediction, proba in zip(metadata.values, predictions, probas):
        from_ip, to_ip, proto, from_port, to_port = row
        buffer = log_ip_flow(from_ip, to_ip, prediction, proba, local_ip)
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
) -> Firewall:
    """
        Firewall factory. Will create a firewall based on the type of firewall that is passed in.
        Currently, this function only supports linux based operating systems

        Args:
            interface - The interface as a string
            interface_data - The interface data as a dictionary
            firewall_type - The name of the firewall to use as a string
            naughty_count - the maximum offenses as an integer

        Returns:
            A firewall if successfully setup, None otherwise
    """
    # Check the firewall type
    if firewall_type == "linux":
        from deepdos.firewall.iptables import IPtable, IPTCError

        try:
            return IPtable(interface, interface_data, naughty_count)
        except IPTCError:
            return None
    else:
        return None

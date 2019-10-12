class MaliciousFlow:
    """
        Tracking malicious flows more efficiently with class containers

        Properties:
            from_ip - The src ip of the malicious flow
            to_ip   - The destination ip of the malicious flow
            from_port - The port spoken from the src ip
            to_port   - The port spoken to at the destination ip
            protocol  - The protocol that was used for communication
            connection - The Full communication (to and from IP)
    """

    def __init__(self, ips, ports, protocol):
        self.from_ip, self.to_ip = ips
        self.from_port, self.to_port = ports
        self.protocol = protocol
        self.connection = f"{self.from_ip}/{self.to_ip}"

    def __repr__(self):
        return f"{self.from_ip}/{self.to_ip}-{self.from_port}:{self.to_port}-{self.protocol}"

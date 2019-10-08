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

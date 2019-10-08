"""
    Lightweight module for keeping track of offenders
"""


class Offender:
    """
        Offender container for connections that are suspicious
    """

    def __init__(self, src, port, protocol, outbound):
        self.src = src
        self.offenses = 1
        self.port_mappings = set()
        self.port_mappings.add((port, protocol))
        self.outbound = outbound

    def add_offense(self, port, protocol):
        """
            Add an offense to the offender
        """
        self.offenses += 1
        self.port_mappings.add((port, protocol))

    def __repr__(self):
        return f"src: {self.src} - off: {self.offenses} - port/proto: {self.port_mappings}, out: {self.outbound}"

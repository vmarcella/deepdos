"""
    Lightweight module for keeping track of offenders
"""


class Offender:
    """
        Offender container for connections that are suspicious

        Args:
            src - 
    """

    def __init__(self, connection, port, protocol, outbound):
        self.connection = connection
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
        return f"src: {self.connection} - off: {self.offenses} - port/proto: {self.port_mappings}, out: {self.outbound}"

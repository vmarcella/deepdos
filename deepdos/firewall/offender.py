"""
    Lightweight module for keeping track of offenders
"""


class Offender:
    """
        Offender container for connections that are suspicious

        Args:
            src - 
    """

    def __init__(
        self,
        connection=None,
        port=None,
        protocol=None,
        outbound=None,
        from_dict=False,
        doc=None,
    ):
        if not from_dict:
            self.connection = connection
            self.offenses = 1
            self.port_mappings = set()
            self.port_mappings.add((port, protocol))
            self.outbound = outbound
        else:
            self.connection = doc["connection"]
            self.offenses = doc["offenses"]
            port_mappings = doc["port_mappings"]
            print(port_mappings)
            self.port_mappings = doc["port_mappings"]
            self.outbound = doc["outbound"]

    def add_offense(self, port, protocol):
        """
            Add an offense to the offender
        """
        self.offenses += 1
        self.port_mappings.add((port, protocol))

    def __repr__(self):
        return f"src: {self.connection} - off: {self.offenses} - port/proto: {self.port_mappings}, out: {self.outbound}"

    @classmethod
    def from_dict(cls, offender_dict):
        return cls(from_dict=True, doc=offender_dict)

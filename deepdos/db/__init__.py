from abc import ABC, abstractmethod


class FirewallDatabase(ABC):
    """
        Abstract database class that all db implementations will  follow
    """

    def __init__(self):
        raise NotImplementedError()

    @abstractmethod
    def register_tables(self):
        """
            Register the necessary tables for the firewall database
        """
        raise NotImplementedError()

    @abstractmethod
    def get_tables(self):
        """
            Get references to the all of the registered tables
        """
        raise NotImplementedError()

    @abstractmethod
    def insert_offender(self, offender_data):
        """
            Insert the offender into the database for tracking
        """
        raise NotImplementedError()

    @abstractmethod
    def remove_offenders(self, banned_offender=None):
        """
            Remove all offenders that are past the expiration time or have been banned
        """
        raise NotImplementedError()

    @abstractmethod
    def insert_banned_output(self, output_data):
        """
            Insert all banned output flows into the the database after banning them
            with the firewall.
        """
        raise NotImplementedError()

    @abstractmethod
    def remove_banned_output(self) -> list:
        """
            Remove all banned output flows from the database.

            Returns:
                A list of the output flows to be removed from the firewall
        """
        raise NotImplementedError()

    @abstractmethod
    def insert_banned_inputs(self, input_data):
        """
           Insert all banned input flows into the database after banning them
           with the firewall.
        """
        raise NotImplementedError()

    @abstractmethod
    def remove_banned_inputs(self) -> list:
        """
            Remove all banned input flows from the database that have expired.

            Returns:
                A list of the input flows to be removed from the firewall
        """
        raise NotImplementedError()

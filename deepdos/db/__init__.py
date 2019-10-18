from abc import ABC, abstractmethod

from deepdos.firewall.offender import Offender


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
    def insert_offender(self, offender: Offender):
        """
            Insert the offender into the database for tracking
        """
        raise NotImplementedError()

    @abstractmethod
    def get_offender(self, offender_connection: str):
        """
            Get an offender given the connection ID
        """
        raise NotImplementedError()

    @abstractmethod
    def update_offender(self, offender: Offender):
        """
            Update an offender in the database
        """
        raise NotImplementedError()

    @abstractmethod
    def remove_offender(self, offender_connection: str):
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

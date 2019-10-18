from deepdos.conf import ETC_DIR
from deepdos.db import FirewallDatabase
from deepdos.firewall.offender import Offender
from tinydb import Query, TinyDB, database

Table = database.Table


class TinyFirewall(FirewallDatabase):
    """
        Firewall database implementation using tinydb! tinydb is written entirely
        in python,allowing a lightweight database system to be utilized by deepdos
        without having any external database software installed.
    
        Properties:
            database - The tinydb database instance.
            offenders_table - The tinydb table instance for all registered offenders.
            input_table - The tinydb table instance for all banned input flows.
            output_table - The tinydb table insance for all banned output flows.
    """

    def __init__(self):
        # Create the database/connection to it
        self.database: database = TinyDB(f"{ETC_DIR}/db/firewall.json")

        # Obtain tables from db
        offender_table, input_table, output_table = self.register_tables()

        # Setup class accessibility to tables
        self.offenders_table: Table = offender_table
        self.input_table: Table = input_table
        self.output_table: Table = output_table

    def register_tables(self) -> (Table, Table, Table):
        """
            Register the tables inside of the TinyDB database

            Returns:
                A tuple of all the created/found tables in your database
        """
        # Create all necessary tables
        offender_table: Table = self.database.table("Offenders")
        input_table: Table = self.database.table("Input")
        output_table: Table = self.database.table("Output")

        return offender_table, input_table, output_table

    def insert_offender(self, offender: Offender):
        """
            Insert an offender into the offenders table
        """
        # Create a query using a query for the offender
        OffenderQ: Query = Query()
        connection_match = OffenderQ.connection == offender.connection

        # Create the document dictionary
        doc: dict = {
            "connection": offender.connection,
            "port_mappings": list(offender.port_mappings),
            "offenses": offender.offenses,
            "outbound": offender.outbound,
        }

        self.offenders_table.insert(doc)

    def update_offender(self, offender: Offender):
        """
            Update an offender in the database
        """

        # Create the document dictionary
        doc: dict = {
            "connection": offender.connection,
            "port_mappings": list(offender.port_mappings),
            "offenses": offender.offenses,
            "outbound": offender.outbound,
        }

        self.offenders_table.update(doc)

    def remove_offender(self, offender_connection: str):
        """
            Remove offenders from the database instance using 
        """
        OffenderQ = Query()
        connection_match = OffenderQ.connection == offender_connection
        self.offenders_table.remove(connection_match)

    def get_offender(self, offender_connection: str) -> Offender:
        """
            Get an offender given the connection ID
        """
        OffenderQ = Query()
        connection_match = OffenderQ.connection == offender_connection
        offender = self.offenders_table.get(connection_match)

        # If an offender is found, return the dict of the offender
        if offender:
            # Remap port_mappings to set.
            offender["port_mappings"] = set(
                [(port, proto) for port, proto in offender["port_mappings"]]
            )
            return Offender.from_dict(offender)

        return None

    def insert_banned_output(self, output_data):
        """
            Insert all banned output flows into the the database after banning them
            with the firewall.
        """
        raise NotImplementedError()

    def remove_banned_output(self) -> list:
        """
            Remove all banned output flows from the database.

            Returns:
                A list of the output flows to be removed from the firewall
        """
        raise NotImplementedError()

    def insert_banned_inputs(self, input_data):
        """
           Insert all banned input flows into the database after banning them
           with the firewall.
        """
        raise NotImplementedError()

    def remove_banned_inputs(self) -> list:
        """
            Remove all banned input flows from the database that have expired.

            Returns:
                A list of the input flows to be removed from the firewall
        """
        raise NotImplementedError()

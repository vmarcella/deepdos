from deepdos.conf import ETC_DIR
from deepdos.db import FirewallDatabase
from tinydb import TinyDB, database

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
        self.database: database = TinyDB("{ETC_DIR}/db/firewall.json")

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

    def insert_offender(self, offender_data: dict):
        """
            Insert an offender into the offenders table
        """
        pass

    def remove_offenders(self, banned_offender: dict = None):
        pass

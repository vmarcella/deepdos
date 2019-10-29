"""
    Analytics db utilizing tinydb
"""
from datetime import datetime

from deepdos.conf import ETC_DIR
from deepdos.db import AnalyticsDatabase
from deepdos.firewall.offender import Offender
from tinydb import Query, TinyDB, database

Table = database.Table


class TinyAnalytics(AnalyticsDatabase):
    """
        Analytics database implementation using tinydb! tinydb is written entirely
        in python, allowing a lightweight database system to be utilized by deepdos
        without having any external database software installed.

    Properties:
            database         - The tinydb database instance.
            offenders_table  - The offenders table.
            exceptions_table - The exception table
    """

    def __init__(self):
        # Create the database/connection to it
        self.database: database = TinyDB(f"{ETC_DIR}/db/analytics.json")

        # Obtain tables from db
        offender_table, errors = self.register_tables()

        # Setup class accessibility to tables
        self.offenders_table: Table = offender_table
        self.exceptions_table: Table = errors

    def register_tables(self) -> (Table, Table):
        """
            Register the tables inside of the TinyDB database

            Returns:
                A tuple of all the created/found tables in your database
        """
        # Create all necessary tables
        offender_table: Table = self.database.table("Offenders")
        errors: Table = self.database.table("Errors")

        return offender_table, errors

    def insert_offender(self, offender: Offender):
        """
            Insert an offender into the offenders table
        """

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

    def insert_exception(self, exception: Exception):
        """
            Insert the exception into the database.

            Args:
                exception - The exception being passed in
        """

        doc: dict = {
            "type": type(exception).__name__,
            "msg": str(exception),
            "time": datetime.today(),
        }
        self.exceptions_table.insert(doc)

"""This file is part of the ETL project for PostgreSQL to Turso migration.

It handles the database connection managers of the source and destination databases.
"""

from sqlalchemy import create_engine


class TursoDBConnectionManager:
    """TursoDBConnectionManager class to manage connections to a Turso database."""

    def __init__(self, sql_connection_string: str, auth_token: str):
        """Initialize the TursoDBConnectionManager with a connection string and authentication token."""
        self.engine = create_engine(
            sql_connection_string,
            connect_args={
                "auth_token": auth_token,
            },
        )

    def get_current_connection(self):
        """Get the current database connection."""
        if not hasattr(self, "connection"):
            self.connection = self.connect()
        return self.connection

    def connect(self):
        """Establish a connection to the Turso database and return the connection object."""
        self.connection = self.engine.connect()
        return self.connection

    def disconnect(self):
        """Close the current database connection."""
        self.connection.close()


class PgSQLDBConnectionManager:
    """PgSQLDBConnectionManager class to manage connections to a PostgreSQL database."""

    def __init__(self, sql_connection_string: str):
        """Initialize the PgSQLDBConnectionManager with a connection string."""
        self.engine = create_engine(sql_connection_string)

    def get_current_connection(self):
        """Get the current database connection, establishing it if necessary."""
        if not hasattr(self, "connection"):
            self.connection = self.connect()
        return self.connection

    def connect(self):
        """Connect to the PostgreSQL database and return the connection object."""
        self.connection = self.engine.connect()
        return self.connection

    def disconnect(self):
        """Close the current database connection."""
        self.connection.close()

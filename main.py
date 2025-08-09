"""ETL application to extract data from a PostgreSQL database and load it into a Turso database."""

import sys

from config.default import *
from core.database_managers.connection_managers import (
    PgSQLDBConnectionManager,
    TursoDBConnectionManager,
)
from core.extract.iam_gateway import get_all_user_roles, get_all_users
from core.load.iam_gateway import User, record_user, record_user_role
from core.models.iam_gateway import UserRole


def configure_app(environment: str) -> tuple[str, str, str]:
    """Configure the application based on the environment.

    This function imports the appropriate configuration based on the environment
    Args:
        environment (str): The environment to configure for ('dev' or 'prod').
    Returns:
        tuple[str, str, str]: A tuple containing the Turso database URL, Turso auth token, and PostgreSQL database URL.
    Raises:
        ValueError: If an invalid environment is specified.
    """
    if environment == "dev":
        from config.localdev import (
            PG_DATABASE_URL,
            TURSO_AUTH_TOKEN,
            TURSO_DATABASE_URL,
        )
    elif environment == "prod":
        from config.prod import (
            PG_DATABASE_URL,
            TURSO_AUTH_TOKEN,
            TURSO_DATABASE_URL,
        )
    else:
        raise ValueError("Invalid environment specified.")
    return TURSO_DATABASE_URL, TURSO_AUTH_TOKEN, PG_DATABASE_URL


def init_databases(
    turso_connection_string: str, turso_auth_token: str, pgsql_connection_string: str
) -> tuple[TursoDBConnectionManager, PgSQLDBConnectionManager]:
    """Initialize the database connection managers for Turso and PostgreSQL.

    Args:
        turso_connection_string (str): The connection string for the Turso database.
        turso_auth_token (str): The authentication token for the Turso database.
        pgsql_connection_string (str): The connection string for the PostgreSQL database.

    Returns:
        tuple[TursoDBConnectionManager, PgSQLDBConnectionManager]: A tuple containing the Turso and PostgreSQL connection managers.
    """
    turso_db_manager = TursoDBConnectionManager(
        sql_connection_string=turso_connection_string, auth_token=turso_auth_token
    )
    pgsql_db_manager = PgSQLDBConnectionManager(
        sql_connection_string=pgsql_connection_string
    )

    return turso_db_manager, pgsql_db_manager


def extract_user_data(connection) -> list[User]:
    """Extract user data from the PostgreSQL database.

    Args:
        connection: The database connection object.
    Returns:
        list[User]: A list of User objects representing all users in the database.
    """
    return get_all_users(connection)


def extract_user_role_data(connection) -> list[UserRole]:
    """Extract user role data from the PostgreSQL database.

    Args:
        connection: The database connection object.
    Returns:
        list[UserRole]: A list of UserRole objects representing all user roles in the database.
    """
    return get_all_user_roles(connection)


def load_user_data(connection, users: list[User]):
    """Load user data into the Turso database.

    This function iterates over a list of User objects and records each user in the database.

    Args:
        connection: The database connection object.
        users: A list of User objects to load into the database.
    """
    for user in users:
        record_user(connection, user, False, True)

    connection.commit()


def load_user_role_data(connection, user_roles: list[UserRole]):
    """Load user role data into the Turso database.

    This function iterates over a list of UserRole objects and records each user role in the database.

    Args:
        connection: The database connection object.
        user_roles: A list of UserRole objects to load into the database.
    """
    for user_role in user_roles:
        # Assuming there's a function to record user roles similar to record_user
        record_user_role(connection, user_role, False)

    connection.commit()


def main(environment: str = "dev"):
    """Launch the ETL process.

    This function configures the application, initializes database connections,
    Args:
        environment (str): The environment to run the ETL process in ('dev' or 'prod').
    """
    turso_connection_string, turso_auth_token, pgsql_connection_string = configure_app(
        environment
    )
    turso_db_manager, pgsql_db_manager = init_databases(
        turso_connection_string, turso_auth_token, pgsql_connection_string
    )

    # Extract data from postgres DB
    users = extract_user_data(pgsql_db_manager.get_current_connection())
    user_roles = extract_user_role_data(pgsql_db_manager.get_current_connection())

    # Load data into TursoDB
    load_user_data(turso_db_manager.get_current_connection(), users)
    load_user_role_data(turso_db_manager.get_current_connection(), user_roles)

    # Close connections
    turso_db_manager.disconnect()
    pgsql_db_manager.disconnect()


if __name__ == "__main__":
    if "dev" in sys.argv:
        environment = "dev"
    elif "prod" in sys.argv:
        environment = "prod"
    else:
        raise ValueError("Please specify 'dev' or 'prod' as an environment argument.")

    print("execute application on environment {}".format(environment))

    main(environment)

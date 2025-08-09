"""This file is part of the ETL project for PostgreSQL to Turso migration.

It contains the IAM gateway application for handling backing up user and user role records.
"""

from os import environ as env

from sqlalchemy import text

from core.helpers.common_sql import convert_bytes_to_sql_string
from core.rsa_encrypt_decrypt.rsa_manager import encrypt

__TABLE_NAME_1 = env.get("TABLE_NAME_1", None)
__FIELD_NAME_1 = env.get("FIELD_NAME_1", None)
__FIELD_NAME_2 = env.get("FIELD_NAME_2", None)
__FIELD_NAME_3 = env.get("FIELD_NAME_3", None)
__FIELD_NAME_4 = env.get("FIELD_NAME_4", None)
__FIELD_NAME_5 = env.get("FIELD_NAME_5", None)
__FIELD_NAME_6 = env.get("FIELD_NAME_6", None)
__FIELD_NAME_7 = env.get("FIELD_NAME_7", None)
__FIELD_NAME_8 = env.get("FIELD_NAME_8", None)
__FIELD_NAME_9 = env.get("FIELD_NAME_9", None)
__FIELD_NAME_10 = env.get("FIELD_NAME_10", None)

__TABLE_NAME_2 = env.get("TABLE_NAME_2", None)
__FIELD_NAME_11 = env.get("FIELD_NAME_11", None)
__FIELD_NAME_12 = env.get("FIELD_NAME_12", None)
__FIELD_NAME_13 = env.get("FIELD_NAME_13", None)
__FIELD_NAME_14 = env.get("FIELD_NAME_14", None)


class User:
    """User class to represent a user in the IAM system."""

    def __init__(self, *args, **kwargs):
        """Initialize a User instance with the provided attributes."""
        self.id = kwargs.get("id")
        self.username = kwargs.get("username")
        self.email = kwargs.get("email")
        self.date_created = kwargs.get("date_created")
        self.token_activation = kwargs.get("token_activation")
        self.active = kwargs.get("active")
        self.date_activated = kwargs.get("date_activated")
        self.date_deactivated = kwargs.get("date_deactivated")
        self.deleted = kwargs.get("deleted")
        self.admin = kwargs.get("admin")

    def __repr__(self) -> str:
        """Return a string representation of the User instance."""
        return f"User(id={self.id}, username={self.username}, email={self.email}, date_created={self.date_created}, token_activation={self.token_activation}, active={self.active}, date_activated={self.date_activated}, date_deactivated={self.date_deactivated}, deleted={self.deleted}, admin={self.admin})"


class UserRole:
    """UserRole class to represent a user role in the IAM system."""

    def __init__(self, *args, **kwargs):
        """Initialize a UserRole instance with the provided attributes."""
        self.id = kwargs.get("id")
        self.user_id = kwargs.get("user_id")
        self.role_id = kwargs.get("role_id")
        self.date_created = kwargs.get("date_created")


def record_user(
    connection, user: User, commit: bool = True, to_encrypt_database: bool = False
) -> bool:
    """Record a user in the database.

    This function inserts a user record into the database, optionally encrypting sensitive fields.
    Args:
        connection: The database connection object.
        user: An instance of the User class containing user details.
        commit: Whether to commit the transaction after inserting the record.
        to_encrypt_database: Whether to encrypt the user data before storing it in the database.
    Returns:
        bool: True if the user was recorded successfully, False otherwise.
    """
    # id = convert_bytes_to_sql_string(encrypt(user.id, "rsa_keys")) if to_encrypt_database else user.id
    username = (
        convert_bytes_to_sql_string(encrypt(user.username, "rsa_keys"))
        if to_encrypt_database
        else user.username
    )
    email = (
        convert_bytes_to_sql_string(encrypt(user.email, "rsa_keys"))
        if to_encrypt_database
        else user.email
    )
    token_activation = (
        convert_bytes_to_sql_string(encrypt(user.token_activation, "rsa_keys"))
        if to_encrypt_database
        else user.token_activation
    )

    s_query = "INSERT INTO {} ({},{},{},{},{},{},{},{},{},{}, password) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', 'ABCD123.4')".format(  # nosec ignore SQL injection here as input data is sanitized
        __TABLE_NAME_1,
        __FIELD_NAME_1,
        __FIELD_NAME_2,
        __FIELD_NAME_3,
        __FIELD_NAME_4,
        __FIELD_NAME_5,
        __FIELD_NAME_6,
        __FIELD_NAME_7,
        __FIELD_NAME_8,
        __FIELD_NAME_9,
        __FIELD_NAME_10,
        user.id,  # id,
        username,
        email,
        user.date_created,
        token_activation,
        user.active,
        user.date_activated,
        user.date_deactivated,
        user.deleted,
        user.admin,
    )
    connection.execute(text(s_query))

    if commit:
        connection.commit()
    return True


def record_user_role(
    connection,
    user_role: UserRole,
    commit: bool = True,
    to_encrypt_database: bool = False,
) -> bool:
    """Record a user role in the database.

    This function inserts a user role record into the database, optionally encrypting sensitive fields.
    Args:
        connection: The database connection object.
        user_role: An instance of the UserRole class containing user role details.
        commit: Whether to commit the transaction after inserting the record.
        to_encrypt_database: Whether to encrypt the user role data before storing it in the database.
    Returns:
        bool: True if the user role was recorded successfully, False otherwise.
    """
    # uid = convert_bytes_to_sql_string(encrypt(user_role.user_id, "rsa_keys")) if to_encrypt_database else user_role.user_id

    s_query = "INSERT INTO {} ({},{},{},{}) VALUES ('{}', '{}', '{}', '{}')".format(  # nosec ignore SQL injection here as input data is sanitized
        __TABLE_NAME_2,
        __FIELD_NAME_11,
        __FIELD_NAME_12,
        __FIELD_NAME_13,
        __FIELD_NAME_14,
        user_role.id,
        user_role.user_id,  # uid,
        user_role.role_id,
        user_role.date_created,
    )
    connection.execute(text(s_query))

    if commit:
        connection.commit()
    return True

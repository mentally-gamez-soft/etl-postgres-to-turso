"""This file is part of the ETL project for PostgreSQL to Turso migration.

It contains the IAM gateway application for handling backing up user and user role records.
"""

from os import environ as env

from sqlalchemy import text

from config.default import (
    FIELD_NAME_1,
    FIELD_NAME_2,
    FIELD_NAME_3,
    FIELD_NAME_4,
    FIELD_NAME_5,
    FIELD_NAME_6,
    FIELD_NAME_7,
    FIELD_NAME_8,
    FIELD_NAME_9,
    FIELD_NAME_10,
    FIELD_NAME_11,
    FIELD_NAME_12,
    FIELD_NAME_13,
    FIELD_NAME_14,
    TABLE_NAME_1,
    TABLE_NAME_2,
)
from core.helpers.common_sql import convert_bytes_to_sql_string
from core.models.iam_gateway import User, UserRole
from core.rsa_encrypt_decrypt.rsa_manager import encrypt


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
        TABLE_NAME_1,
        FIELD_NAME_1,
        FIELD_NAME_2,
        FIELD_NAME_3,
        FIELD_NAME_4,
        FIELD_NAME_5,
        FIELD_NAME_6,
        FIELD_NAME_7,
        FIELD_NAME_8,
        FIELD_NAME_9,
        FIELD_NAME_10,
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
        TABLE_NAME_2,
        FIELD_NAME_11,
        FIELD_NAME_12,
        FIELD_NAME_13,
        FIELD_NAME_14,
        user_role.id,
        user_role.user_id,  # uid,
        user_role.role_id,
        user_role.date_created,
    )
    connection.execute(text(s_query))

    if commit:
        connection.commit()
    return True

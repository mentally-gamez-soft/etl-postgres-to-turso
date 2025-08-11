"""This module provides functions to extract user and user role data from a source database."""

import logging

from sqlalchemy import text

from config.default import (
    FIELD_NAME_2,
    FIELD_NAME_3,
    FIELD_NAME_4,
    FIELD_NAME_5,
    FIELD_NAME_6,
    FIELD_NAME_7,
    FIELD_NAME_8,
    FIELD_NAME_9,
    FIELD_NAME_10,
    FIELD_NAME_12,
    FIELD_NAME_13,
    FIELD_NAME_14,
    TABLE_NAME_1,
    TABLE_NAME_2,
)
from core.models.iam_gateway import User, UserRole

logger = logging.getLogger("__main__")


def get_all_users(connection) -> list[User]:
    """Fetch all users from the database.

    This function retrieves all user records from the database and returns them as a list of User objects.
    Args:
        connection: The database connection object.
    Returns:
        list[User]: A list of User objects representing all users in the database.
    """
    result = connection.execute(
        text(
            f"SELECT id, {FIELD_NAME_2}, {FIELD_NAME_3}, {FIELD_NAME_4}, {FIELD_NAME_5}, {FIELD_NAME_6}, {FIELD_NAME_7}, {FIELD_NAME_8}, {FIELD_NAME_9}, {FIELD_NAME_10} FROM {TABLE_NAME_1}"  # nosec ignore SQL injection risk, as the input data is sanitized
        )
    ).fetchall()
    logger.info("All users have been retrieved from %s", TABLE_NAME_1)
    return [
        User(
            **{
                "id": user.id,
                "username": user.__getattribute__(FIELD_NAME_2),
                "email": user.__getattribute__(FIELD_NAME_3),
                "date_created": user.__getattribute__(FIELD_NAME_4),
                "token_activation": user.__getattribute__(FIELD_NAME_5),
                "active": user.__getattribute__(FIELD_NAME_6),
                "date_activated": user.__getattribute__(FIELD_NAME_7),
                "date_deactivated": user.__getattribute__(FIELD_NAME_8),
                "deleted": user.__getattribute__(FIELD_NAME_9),
                "admin": user.__getattribute__(FIELD_NAME_10),
            }
        )
        for user in result
    ]


def get_all_user_roles(connection) -> list[UserRole]:
    """Fetch all user roles from the database.

    This function retrieves all user role records from the database and returns them as a list of UserRole objects.
    Args:
        connection: The database connection object.
    Returns:
        list[UserRole]: A list of UserRole objects representing all user roles in the database.
    """
    result = connection.execute(
        text(
            f"SELECT id, {FIELD_NAME_12}, {FIELD_NAME_13}, {FIELD_NAME_14} FROM {TABLE_NAME_2}"  # nosec ignore SQL injection risk, as the input data is sanitized
        )
    ).fetchall()
    logger.info("All user roles have been retrieved from %s", TABLE_NAME_2)
    return [
        UserRole(
            **{
                "id": role.id,
                "user_id": role.__getattribute__(FIELD_NAME_12),
                "role_id": role.__getattribute__(FIELD_NAME_13),
                "date_created": role.__getattribute__(FIELD_NAME_14),
            }
        )
        for role in result
    ]

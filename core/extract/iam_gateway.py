"""This module provides functions to extract user and user role data from a source database."""

from os import environ as env

from sqlalchemy import text

from core.models.iam_gateway import User, UserRole

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
            f"SELECT id, {__FIELD_NAME_2}, {__FIELD_NAME_3}, {__FIELD_NAME_4}, {__FIELD_NAME_5}, {__FIELD_NAME_6}, {__FIELD_NAME_7}, {__FIELD_NAME_8}, {__FIELD_NAME_9}, {__FIELD_NAME_10} FROM {__TABLE_NAME_1}"  # nosec ignore SQL injection risk, as the input data is sanitized
        )
    ).fetchall()
    return [
        User(
            **{
                "id": user.id,
                "username": user.__getattribute__(__FIELD_NAME_2),
                "email": user.__getattribute__(__FIELD_NAME_3),
                "date_created": user.__getattribute__(__FIELD_NAME_4),
                "token_activation": user.__getattribute__(__FIELD_NAME_5),
                "active": user.__getattribute__(__FIELD_NAME_6),
                "date_activated": user.__getattribute__(__FIELD_NAME_7),
                "date_deactivated": user.__getattribute__(__FIELD_NAME_8),
                "deleted": user.__getattribute__(__FIELD_NAME_9),
                "admin": user.__getattribute__(__FIELD_NAME_10),
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
            f"SELECT id, {__FIELD_NAME_12}, {__FIELD_NAME_13}, {__FIELD_NAME_14} FROM {__TABLE_NAME_2}"  # nosec ignore SQL injection risk, as the input data is sanitized
        )
    ).fetchall()
    return [
        UserRole(
            **{
                "id": role.id,
                "user_id": role.__getattribute__(__FIELD_NAME_12),
                "role_id": role.__getattribute__(__FIELD_NAME_13),
                "date_created": role.__getattribute__(__FIELD_NAME_14),
            }
        )
        for role in result
    ]

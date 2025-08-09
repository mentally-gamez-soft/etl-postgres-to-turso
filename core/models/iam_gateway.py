"""This module defines the User and UserRole classes for the IAM system.

These classes represent users and their roles within the system.
It includes methods for initializing user and role instances with their attributes.
"""


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

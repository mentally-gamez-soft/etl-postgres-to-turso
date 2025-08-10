"""Base test class for unit tests in the ETL project.

It provides common setup and teardown methods for tests.
"""

import unittest
from os import environ as env

from faker import Faker
from sqlalchemy import text

from config.testing import *
from core.database_managers.connection_managers import (
    PgSQLDBConnectionManager,
    TursoDBConnectionManager,
)
from core.load.iam_gateway import record_user, record_user_role, set_timestamp
from core.models.iam_gateway import User, UserRole


class BaseTestClass(unittest.TestCase):
    """
    Base class for all test cases.

    Provides common setup and teardown methods.
    """

    def setUp(self):
        """Set up the test environment before each test."""
        self.fake = Faker()
        self.users = self.create_fake_users(2)
        self.roles = self.create_fake_user_roles(2)

        self.turso_db_manager = TursoDBConnectionManager(
            sql_connection_string=TURSO_DATABASE_URL, auth_token=TURSO_AUTH_TOKEN
        )
        self.turso_connection = self.turso_db_manager.get_current_connection()
        self.truncate_all_load_database()

        self.pg_db_manager = PgSQLDBConnectionManager(
            sql_connection_string=PG_DATABASE_URL
        )
        self.pg_connection = self.pg_db_manager.get_current_connection()
        self.truncate_all_export_database()
        self.users_n_roles = self.get_all_users_and_roles()

        # Insert random datasets to the databases
        self.initialize_fake_data()

    def tearDown(self):
        """Clean up the test environment after each test."""
        # Release any resources used in tests
        del self.users
        del self.roles
        self.turso_db_manager.disconnect()
        self.pg_db_manager.disconnect()

    def create_fake_user(self):
        """
        Create a fake user using Faker.

        Returns a dictionary representing the user.
        """
        return User(
            **{
                "id": str(self.fake.uuid4()),
                "username": self.fake.user_name(),
                "email": self.fake.email(),
                "date_created": self.fake.date_time_this_year().isoformat(),
                "token_activation": str(self.fake.uuid4()),
                "active": self.fake.boolean(),
                "date_activated": self.fake.date_time_this_year().isoformat(),
                "date_deactivated": self.fake.date_time_this_year().isoformat(),
                "deleted": self.fake.boolean(),
                "admin": self.fake.boolean(),
            }
        )

    def truncate_all_load_database(self):
        """Truncate all tables in the load database."""
        # self.connection.execute(text(f"DELETE FROM {TABLE_NAME_2}"))
        self.turso_connection.execute(text(f"DELETE FROM {TABLE_NAME_1}"))
        self.turso_connection.commit()

    def truncate_all_export_database(self):
        """Truncate all tables in the export database."""
        self.pg_connection.execute(text(f"DELETE FROM {TABLE_NAME_2}"))
        self.pg_connection.execute(text(f"DELETE FROM {TABLE_NAME_1}"))
        self.pg_connection.commit()

    def initialize_fake_data(self):
        """Initialize fake data for testing."""
        for user in self.users:
            record_user(self.turso_connection, user, False, True)
            record_user(self.pg_connection, user, False)

        for role in self.roles:
            record_user_role(self.turso_connection, role, False, True)
            record_user_role(self.pg_connection, role, False)
        self.turso_connection.commit()
        self.pg_connection.commit()

        set_timestamp(self.turso_connection)

    def create_fake_users(self, num_users=5):
        """
        Create fake users using Faker.

        Returns a list of dictionaries representing the users.
        """
        users = []
        for _ in range(num_users):
            user = self.create_fake_user()
            users.append(user)
        return users

    def create_fake_user_roles(self, num_roles=5):
        """
        Create fake user roles using Faker.

        Returns a list of dictionaries representing the user roles.
        """
        user_roles = []
        for _ in range(num_roles):
            user_role = UserRole(
                **{
                    "id": self.fake.random_number(digits=5),
                    "user_id": self.users[_].id,
                    "role_id": self.fake.job().capitalize(),
                    "date_created": self.fake.date_time_this_year().isoformat(),
                }
            )
            user_roles.append(user_role)
        return user_roles

    def get_all_users_and_roles(self) -> tuple[list[User], list[UserRole]]:
        """
        Fetch all users and roles from the database.

        Returns a tuple of lists containing users and roles.
        """
        users = self.pg_connection.execute(
            text(
                f"SELECT id, {FIELD_NAME_2}, {FIELD_NAME_3}, {FIELD_NAME_4}, {FIELD_NAME_5}, {FIELD_NAME_6}, {FIELD_NAME_7}, {FIELD_NAME_8}, {FIELD_NAME_9}, {FIELD_NAME_10} FROM {TABLE_NAME_1}"
            )
        ).all()

        l_users = [
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
            for user in users
        ]

        roles = self.pg_connection.execute(
            text(
                f"SELECT id, {FIELD_NAME_12}, {FIELD_NAME_13}, {FIELD_NAME_14} FROM {TABLE_NAME_2}"
            )
        ).all()
        l_roles = [
            UserRole(
                **{
                    "id": role.id,
                    "user_id": role.__getattribute__(FIELD_NAME_12),
                    "role_id": role.__getattribute__(FIELD_NAME_13),
                    "date_created": role.__getattribute__(FIELD_NAME_14),
                }
            )
            for role in roles
        ]
        return l_users, l_roles

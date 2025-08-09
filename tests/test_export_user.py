from config.default import (
    FIELD_NAME_2,
    FIELD_NAME_3,
    FIELD_NAME_12,
    FIELD_NAME_13,
)
from core.extract.iam_gateway import get_all_user_roles, get_all_users
from tests import BaseTestClass


class TestExportUser(BaseTestClass):
    """
    Test case for exporting user data.
    """

    def test_export_users_and_roles(self):
        """Test the export of user data."""
        users, roles = self.get_all_users_and_roles()

        self.assertIsNotNone(users)
        rand_index = self.fake.random_int(min=0, max=len(users) - 1)
        self.assertEqual(
            users[rand_index].__getattribute__(FIELD_NAME_2),
            self.users[rand_index].username,
        )
        self.assertEqual(
            users[rand_index].__getattribute__(FIELD_NAME_3),
            self.users[rand_index].email,
        )

        self.assertIsNotNone(roles)
        rand_index = self.fake.random_int(min=0, max=len(roles) - 1)
        self.assertEqual(
            str(roles[rand_index].user_id),
            self.roles[rand_index].user_id,
        )
        self.assertEqual(
            roles[rand_index].role_id,
            self.roles[rand_index].role_id,
        )

    def test_export_users_from_source_db(self):
        """Test the export of users from the source database."""
        users = get_all_users(self.pg_connection)

        self.assertIsNotNone(users)
        rand_index = self.fake.random_int(min=0, max=len(users) - 1)
        self.assertEqual(
            users[rand_index].__getattribute__(FIELD_NAME_2),
            self.users[rand_index].username,
        )
        self.assertEqual(
            users[rand_index].__getattribute__(FIELD_NAME_3),
            self.users[rand_index].email,
        )

    def test_export_user_roles_from_source_db(self):
        """
        Test the export of user roles from the source database.
        """
        roles = get_all_user_roles(self.pg_connection)

        self.assertIsNotNone(roles)
        rand_index = self.fake.random_int(min=0, max=len(roles) - 1)
        self.assertEqual(
            str(roles[rand_index].user_id),
            self.roles[rand_index].user_id,
        )
        self.assertEqual(
            roles[rand_index].role_id,
            self.roles[rand_index].role_id,
        )

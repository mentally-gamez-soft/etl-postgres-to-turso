from config.default import (
    FIELD_NAME_2,
    FIELD_NAME_3,
    FIELD_NAME_12,
    FIELD_NAME_13,
)
from tests import BaseTestClass


class TestExportUser(BaseTestClass):
    """
    Test case for exporting user data.
    """

    def test_export_users_and_roles(self):
        """
        Test the export of user data.
        """
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
            roles[rand_index].__getattribute__(FIELD_NAME_12),
            self.roles[rand_index].user_id,
        )
        self.assertEqual(
            roles[rand_index].__getattribute__(FIELD_NAME_13),
            self.roles[rand_index].role_id,
        )

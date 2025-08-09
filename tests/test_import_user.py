import unittest

from sqlalchemy import text

from config.default import FIELD_NAME_1, FIELD_NAME_5
from core.helpers.common_sql import convert_sql_string_to_bytes
from core.rsa_encrypt_decrypt.rsa_manager import decrypt
from tests import (
    FIELD_NAME_2,
    FIELD_NAME_3,
    FIELD_NAME_12,
    FIELD_NAME_13,
    TABLE_NAME_1,
    TABLE_NAME_2,
    BaseTestClass,
)


class TestImportUser(BaseTestClass):

    def test_import_user_in_postgres_DB(self):
        """
        Test the import of a user in pg db.
        """
        # Fetch the user back from the database to verify
        fetched_user = self.pg_connection.execute(
            text(f"SELECT * FROM {TABLE_NAME_1} WHERE id = :id"),
            {"id": self.users[0].id},
        ).all()

        self.assertIsNotNone(fetched_user)
        self.assertEqual(
            fetched_user[0].__getattribute__(FIELD_NAME_5),
            self.users[0].token_activation,
        )
        self.assertEqual(
            fetched_user[0].__getattribute__(FIELD_NAME_2), self.users[0].username
        )
        self.assertEqual(
            fetched_user[0].__getattribute__(FIELD_NAME_3), self.users[0].email
        )

    def test_import_user_in_turso_backup_DB(self):
        """
        Test the import of a user in turso backup db.
        """
        # Fetch the user back from the database to verify
        fetched_user = self.turso_connection.execute(
            text(f"SELECT * FROM {TABLE_NAME_1} WHERE id = :id"),
            {"id": self.users[0].id},
        ).all()

        self.assertIsNotNone(fetched_user)
        # self.assertEqual(
        #     decrypt(convert_sql_string_to_bytes(fetched_user[0].__getattribute__(FIELD_NAME_1)),"rsa_keys"), self.users[0].id
        # )
        self.assertEqual(
            decrypt(
                convert_sql_string_to_bytes(
                    fetched_user[0].__getattribute__(FIELD_NAME_5)
                ),
                "rsa_keys",
            ).decode(),
            self.users[0].token_activation,
        )
        self.assertEqual(
            decrypt(
                convert_sql_string_to_bytes(
                    fetched_user[0].__getattribute__(FIELD_NAME_2)
                ),
                "rsa_keys",
            ).decode(),
            self.users[0].username,
        )
        self.assertEqual(
            decrypt(
                convert_sql_string_to_bytes(
                    fetched_user[0].__getattribute__(FIELD_NAME_3)
                ),
                "rsa_keys",
            ).decode(),
            self.users[0].email,
        )

    def test_import_roles(self):
        """
        Test the import of user roles.
        """
        # Fetch the role back from the database to verify
        fetched_role = self.turso_connection.execute(
            text(f"SELECT * FROM {TABLE_NAME_2} WHERE id = :id"),
            {"id": self.roles[0].id},
        ).all()

        self.assertIsNotNone(fetched_role)
        self.assertEqual(
            fetched_role[0].__getattribute__(FIELD_NAME_12), self.roles[0].user_id
        )
        self.assertEqual(
            fetched_role[0].__getattribute__(FIELD_NAME_13), self.roles[0].role_id
        )

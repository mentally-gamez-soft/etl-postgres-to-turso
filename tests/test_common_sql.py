import unittest

import faker

from core.helpers.common_sql import (
    convert_bytes_to_sql_string,
    convert_sql_string_to_bytes,
)
from core.rsa_encrypt_decrypt.rsa_manager import decrypt, encrypt


class TestCommonSQL(unittest.TestCase):
    def _get_fake_messages(self, n=30):
        fake = faker.Faker()
        return [fake.sentence() for _ in range(n)]

    def setUp(self):
        self.fake = faker.Faker()
        self.list_of_messages = self._get_fake_messages(10)

    def test_rsa_encrypted_bytes_to_sql_string(self):
        """
        Test that RSA encrypted data can be converted to a SQL string.
        """
        for message in self.list_of_messages:
            encrypted_data = encrypt(message, "rsa_keys")
            sql_string = convert_bytes_to_sql_string(encrypted_data)
            self.assertIsInstance(sql_string, str)
            self.assertNotEqual(message, sql_string)

            if b"'" in encrypted_data:
                self.assertIn("SINGLE_QUOTE", sql_string)
            if b":" in encrypted_data:
                self.assertIn("COLON", sql_string)

            sql_bytes = convert_sql_string_to_bytes(sql_string)
            self.assertIsInstance(sql_bytes, bytes)
            self.assertEqual(encrypted_data, sql_bytes)
            decrypted_data = decrypt(sql_bytes, "rsa_keys")
            self.assertEqual(message, decrypted_data.decode("utf-8"))

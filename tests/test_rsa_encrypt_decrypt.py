import unittest

from config.testing import *
from core.rsa_encrypt_decrypt.rsa_manager import decrypt, encrypt


class TestRsaManager(unittest.TestCase):

    def test_encrypt_decode(self):
        original_data = "322e6085-360e-4f4a-8935-40259ea4cd74"
        encrypted_data = encrypt(original_data, "rsa_keys")
        self.assertIsInstance(encrypted_data, bytes)
        self.assertNotEqual(original_data, encrypted_data)

    def test_encrypt_uid(self):
        original_data = "322e6085-360e-4f4a-8935-40259ea4cd74"
        encrypted_data = encrypt(original_data, "rsa_keys")

        self.assertIsInstance(encrypted_data, bytes)
        self.assertNotEqual(original_data.encode("utf-8"), encrypted_data)

    def test_decrypt_uid(self):
        original_data = "322e6085-360e-4f4a-8935-40259ea4cd74"
        encrypted_data = encrypt(original_data, "rsa_keys")
        decrypted_data = decrypt(encrypted_data, "rsa_keys").decode("utf-8")

        self.assertEqual(original_data, decrypted_data)

    def test_encrypt_uname(self):
        original_data = "rubiobryce"
        encrypted_data = encrypt(original_data, "rsa_keys")

        self.assertIsInstance(encrypted_data, bytes)
        self.assertNotEqual(original_data.encode("utf-8"), encrypted_data)

    def test_decrypt_uname(self):
        original_data = "rubiobryce"
        encrypted_data = encrypt(original_data, "rsa_keys")
        decrypted_data = decrypt(encrypted_data, "rsa_keys").decode("utf-8")

        self.assertEqual(original_data, decrypted_data)

    def test_encrypt_umail(self):
        original_data = "wesley92@example.com"
        encrypted_data = encrypt(original_data, "rsa_keys")

        self.assertIsInstance(encrypted_data, bytes)
        self.assertNotEqual(original_data.encode("utf-8"), encrypted_data)

    def test_decrypt_umail(self):
        original_data = "wesley92@example.com"
        encrypted_data = encrypt(original_data, "rsa_keys")
        decrypted_data = decrypt(encrypted_data, "rsa_keys").decode("utf-8")

        self.assertEqual(original_data, decrypted_data)

    def test_encrypt_token(self):
        original_data = "c965a68a-de64-4913-8c7a-4f2cb276af82"
        encrypted_data = encrypt(original_data, "rsa_keys")

        self.assertIsInstance(encrypted_data, bytes)
        self.assertNotEqual(original_data.encode("utf-8"), encrypted_data)

    def test_decrypt_token(self):
        original_data = "c965a68a-de64-4913-8c7a-4f2cb276af82"
        encrypted_data = encrypt(original_data, "rsa_keys")
        decrypted_data = decrypt(encrypted_data, "rsa_keys").decode("utf-8")

        self.assertEqual(original_data, decrypted_data)

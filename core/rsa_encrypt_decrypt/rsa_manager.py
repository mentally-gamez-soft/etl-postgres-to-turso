"""This module provides functions to manage RSA encryption and decryption.

It includes functions to generate, store, read keys, and encrypt/decrypt messages.
"""

import os

import rsa
from rsa import PrivateKey, PublicKey

from config.default import BASE_DIR


def generate_keys(bits: int = 2048) -> tuple[PublicKey, PrivateKey]:
    """Generate a pair of RSA keys.

    This function generates a public and private key pair using RSA encryption.
    Args:
        bits (int): The number of bits for the key size. Default is 2048.
    Returns:
        tuple: A tuple containing the public and private keys.
    """
    public_key, private_key = rsa.newkeys(bits)
    return public_key, private_key


def store_keys(public_key: PublicKey, private_key: PrivateKey, key_path: str) -> None:
    """Store the RSA keys to files.

    This function saves the public and private keys to specified files in the given directory.
    Args:
        public_key (PublicKey): The public key to store.
        private_key (PrivateKey): The private key to store.
        key_path (str): The directory path where the keys will be stored.
    """
    with open(os.path.join(BASE_DIR, key_path, "public_key.pem"), "wb") as pub_file:
        pub_file.write(public_key.save_pkcs1("PEM"))
    with open(os.path.join(BASE_DIR, key_path, "private_key.pem"), "wb") as priv_file:
        priv_file.write(private_key.save_pkcs1("PEM"))


def read_keys(key_path: str) -> tuple[PublicKey, PrivateKey]:
    """Read RSA keys from files.

    This function reads the public and private keys from specified files in the given directory.
    Args:
        key_path (str): The directory path where the keys are stored.
    Returns:
        tuple: A tuple containing the public and private keys.
    """
    with open(os.path.join(BASE_DIR, key_path, "public_key.pem"), "rb") as pub_file:
        public_key = PublicKey.load_pkcs1(pub_file.read(), "PEM")
    with open(os.path.join(BASE_DIR, key_path, "private_key.pem"), "rb") as priv_file:
        private_key = PrivateKey.load_pkcs1(priv_file.read(), "PEM")
    return public_key, private_key


def encrypt(message: str, key_path: str) -> bytes:
    """Encrypt a message using the public key.

    This function encrypts a given message using the public key stored in the specified directory.
    Args:
        message (str): The message to encrypt.
        key_path (str): The directory path where the public key is stored.
    Returns:
        bytes: The encrypted message as bytes.
    """
    if not os.path.exists(os.path.join(BASE_DIR, key_path, "public_key.pem")):
        store_keys(*generate_keys(), os.path.join(BASE_DIR, key_path))
    public_key, _ = read_keys(key_path)
    return rsa.encrypt(message.encode("utf-8"), public_key)


def decrypt(encrypted_message: bytes, key_path: str) -> bytes:
    """Decrypt a message using the private key.

    This function decrypts a given encrypted message using the private key stored in the specified directory.
    Args:
        encrypted_message (bytes): The encrypted message to decrypt.
        key_path (str): The directory path where the private key is stored.
    Returns:
        bytes: The decrypted message as bytes.
    """
    if not os.path.exists(os.path.join(BASE_DIR, key_path, "private_key.pem")):
        raise FileNotFoundError("Key files not found. Please generate keys first.")
    _, private_key = read_keys(key_path)
    return rsa.decrypt(encrypted_message, private_key)

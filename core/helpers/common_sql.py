"""This module provides utility functions to convert between bytes and SQL string representations.

It includes functions to convert encrypted data to a SQL string and vice versa.
"""

import codecs

_SINGLE_QUOTE = "SINGLE_QUOTE"
_COLON = "COLON"


def convert_bytes_to_sql_string(encrypted_data: bytes) -> str:
    """
    Convert bytes to a SQL string representation.

    This function replaces single quotes and colons in the byte string to ensure it can be safely used in SQL queries.
    Args:
        encrypted_data (bytes): The bytes to convert.
    Returns:
        str: The SQL string representation of the bytes.
    """
    s_encrypted_data = str(encrypted_data)[2:-1]
    s_encrypted_data = s_encrypted_data.replace("'", _SINGLE_QUOTE).replace(":", _COLON)
    return s_encrypted_data


def convert_sql_string_to_bytes(sql_string: str) -> bytes:
    """
    Convert a SQL string representation back to bytes.

    This function reverses the conversion done by `convert_bytes_to_sql_string`.
    Args:
        sql_string (str): The SQL string to convert.
    Returns:
        bytes: The original bytes.
    """
    sql_string = sql_string.replace(_SINGLE_QUOTE, "'").replace(_COLON, ":")
    return codecs.escape_decode(r"{}".format(sql_string))[
        0
    ]  # Using escape_decode to handle any special characters

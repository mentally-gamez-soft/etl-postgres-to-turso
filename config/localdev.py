"""Load the configuration for local environment.

Raises:
    Exception: Raise an error if the .env file for local environment does not exist.
"""

from dotenv import load_dotenv

from .default import *

if not load_dotenv(join(ENV_DIR, ".local.env")):
    raise Exception("Failed to load .local.env file !!!")

TURSO_DB = env["TURSO_DATABASE"]
TURSO_DATABASE_URL = env["TURSO_CONNECTION_STRING"]
TURSO_AUTH_TOKEN = env["TURSO_TOKEN_AUTH"]
PG_DATABASE_URL = env["SQLALCHEMY_DATABASE_URI"]

# Logs
LOG_LEVEL = "INFO"

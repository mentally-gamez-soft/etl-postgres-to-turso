"""Load the configuration for prod environment.

Raises:
    Exception: Raise an error if the .env file for prod environment does not exist.
"""

from dotenv import load_dotenv

from .default import *

if not load_dotenv(join(ENV_DIR, ".prod.env")):
    raise Exception("Failed to load .prod.env file !!!")

TURSO_DB = env["TURSO_DATABASE"]
TURSO_DATABASE_URL = env["TURSO_CONNECTION_STRING"]
TURSO_AUTH_TOKEN = env["TURSO_TOKEN_AUTH"]
PG_DATABASE_URL = env["SQLALCHEMY_DATABASE_URI"]

# Logs
LOG_LEVEL = "INFO"

"""Load the default configuration for all environments.

Raises:
    Exception: Raise an error if the .env file does not exist.
"""

from os import environ as env
from os.path import abspath, dirname, join

from dotenv import load_dotenv

# Define the application directory
BASE_DIR = dirname(dirname(abspath(__file__)))

ENV_DIR = join(BASE_DIR, "config")

if not load_dotenv(join(ENV_DIR, ".env")):
    raise Exception("Failed to load .env file !!!")

# Application information
APP_NAME = env.get("APP_NAME", "MyApp")
APP_VERSION = env.get("APP_VERSION", "0.0.1")

# Logs
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# database configuration
TABLE_NAME_1 = env["TABLE_NAME_1"]
FIELD_NAME_1 = env["FIELD_NAME_1"]
FIELD_NAME_2 = env["FIELD_NAME_2"]
FIELD_NAME_3 = env["FIELD_NAME_3"]
FIELD_NAME_4 = env["FIELD_NAME_4"]
FIELD_NAME_5 = env["FIELD_NAME_5"]
FIELD_NAME_6 = env["FIELD_NAME_6"]
FIELD_NAME_7 = env["FIELD_NAME_7"]
FIELD_NAME_8 = env["FIELD_NAME_8"]
FIELD_NAME_9 = env["FIELD_NAME_9"]
FIELD_NAME_10 = env["FIELD_NAME_10"]
TABLE_NAME_2 = env["TABLE_NAME_2"]
FIELD_NAME_11 = env["FIELD_NAME_11"]
FIELD_NAME_12 = env["FIELD_NAME_12"]
FIELD_NAME_13 = env["FIELD_NAME_13"]
FIELD_NAME_14 = env["FIELD_NAME_14"]

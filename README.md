# =============================
# ETL Postgres to Turso 
# =============================
Application for migrating data from a Postgres database to a Turso database.

## Requirements
- Python 3.11 or higher
- pip 24.0 or higher
- virtualenv 20.16.7 or higher
- uv 0.4.0 or higher
- docker 20.10.21 or higher
- docker-compose 1.29.2 or higher

## Stack Technologies
![Alt text](stack-techno-backup-DB.svg)

## Running application
## Local development
    uv run main.py [prod|dev]

### Executing the tests suit
    uv run -m unittest tests.test_common_sql
    uv run -m unittest tests.test_rsa_encrypt_decrypt
    uv run -m unittest tests.test_import_user
    uv run -m unittest tests.test_export_user

## Docker Images
### Create an image
    On unix OS:
    execute the shell ./docker_manager.sh choose option (1) and follow the instructions.

    On windows OS:
    execute the shell ./docker_manager.ps1 choose option (1) and follow the instructions.

### Run a container
    On unix OS:
    execute the shell ./docker_manager.sh choose option (2) and follow the instructions.

    On windows OS:
    execute the shell ./docker_manager.ps1 choose option (2) and follow the instructions.

### Stop a container
    On unix OS:
    execute the shell ./docker_manager.sh choose option (3) and follow the instructions.

    On windows OS:
    execute the shell ./docker_manager.ps1 choose option (3) and follow the instructions.



"""
settings.py

This module contains configurations for various components
of the application.

Configurations:

MongoDB:
- MONGODB_CONNECTION: Contains configurations for connecting to
                      the MongoDB instance.
    
File paths:
- PREFILL_FILES: Specifies the paths to the JSON files containing
                 initial seeding data for the database.
                 This data is later used in _db_prefill.py module.

Logging:
- EVENT_LOG_FORMAT: The format of log messages for event log.
- ERROR_LOG_FORMAT: The format of log messages for error log.
- BACKUP_LOG_COUNT: The number of backup log files to retain.

GraphQL settings:
- RECURSION_DEPTH: Determines the depth of nested queries before
                   returning simpler data. Beyond this depth,
                   only IDs are returned instead of full objects.
"""

from pathlib import Path

from decouple import config


# MongoDB configurations
MONGODB_CONNECTION = {
    'host': config('MONGODB_HOST'),
    'port': int(config('MONGODB_PORT')),
    'db': config('MONGODB_DB'),
    # 'username': config('MONGODB_USERNAME'),
    # 'password': config('MONGODB_PASSWORD'),
}

# File paths
PREFILL_FILES = {
    'characters': Path('initial_data') / 'characters.json',
    'powers': Path('initial_data') / 'powers.json',
}

# Logging configurations
EVENT_LOG_FORMAT = '%(asctime)s: [%(levelname)s] %(message)s'
ERROR_LOG_FORMAT = '%(asctime)s: [%(levelname)s] [%(name)s] %(message)s'
BACKUP_LOG_COUNT = 5

# GraphQL settings
RECURSION_DEPTH = 4 

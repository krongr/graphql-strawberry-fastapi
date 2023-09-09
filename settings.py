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

# Paths to JSON files containing initial seeding data for the database.
PREFILL_FILES = {
    'characters': Path('initial_data') / 'characters.json',
    'powers': Path('initial_data') / 'powers.json',
}

# Logging configurations
EVENT_LOG_FORMAT = '%(asctime)s: [%(levelname)s] %(message)s'
ERROR_LOG_FORMAT = '%(asctime)s: [%(levelname)s] [%(module)s] %(message)s'
BACKUP_LOG_COUNT = 5

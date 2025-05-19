import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def get_data_path(*path_parts):
    return os.path.join(PROJECT_ROOT, 'data', *path_parts)
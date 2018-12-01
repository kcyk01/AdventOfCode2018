import os


def get_input(file_name: str) -> str:
    if not os.path.exists(file_name):
        raise FileNotFoundError
    with open(file_name, 'r') as f:
        return f.read()

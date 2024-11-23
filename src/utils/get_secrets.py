import os
from dotenv import load_dotenv
from pathlib import Path


# Load environment variables from a .env file
def load_env_file():
    """
    Load environment variables from the project root .env file
    """
    project_root = Path(
        __file__
    ).parent.parent.parent
    env_file = project_root / ".env"

    if not env_file.exists():
        raise FileNotFoundError(f"The .env file was not found at: {env_file.resolve()}")

    load_dotenv(dotenv_path=env_file)
    print(f"Environment variables loaded from: {env_file.resolve()}")

def get_env_variable(key, default=None):
    """
    Retrieve the value of an environment variable
    """
    value = os.getenv(key, default)
    if value is None:
        print(
            f"Warning: Environment variable '{key}' not found. Using default: {default}"
        )
    return value

try:
    load_env_file()
except FileNotFoundError as e:
    print(f"Error: {e}")

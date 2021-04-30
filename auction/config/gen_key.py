import os
from django.core.management.utils import get_random_secret_key

# Generates a file with a secret key. Temporary solution;
# environment variable should be used instead.
def gen_key():
    try:
        from .secret_key import SECRET_KEY
        return SECRET_KEY
    except ModuleNotFoundError:
        SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))
        generate_secret_key(os.path.join(SETTINGS_DIR, 'secret_key.py'))
        from .secret_key import SECRET_KEY
        return SECRET_KEY


def generate_secret_key(filepath):
    secret_file = open(filepath, "w")
    secret = "SECRET_KEY= " + "\"" + get_random_secret_key() + "\"" + "\n"
    secret_file.write(secret)
    secret_file.close()

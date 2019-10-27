from configparser import ConfigParser
from github_reporter import timestamp
from os import environ
from os.path import abspath, dirname, exists, join
from sys import exit, stderr

CONFIG_FILENAME = "setup.cfg"
CONFIG_SECTION_NAME = "github_reporter"
CONFIG_KEYS = (
    "base_page_title",
    "github_repo_name",
    "branch",
    "github_org",
    "timezone",
)
SECRET_ENV_VARS = ("GITHUB_TOKEN", "GITHUB_ORGANIZATION")
SECRETS_FILENAME = "secrets.json"
HERE = abspath(dirname(dirname(__file__)))


def load_config():
    parser = ConfigParser()
    parser.read(join(HERE, CONFIG_FILENAME))
    config = parser[CONFIG_SECTION_NAME]
    misconf = False
    if not all([key in config for key in CONFIG_KEYS]):
        msg = f"{CONFIG_KEYS} must all be defined in config.json."
        misconf = True
    if any([key not in CONFIG_KEYS for key in config.keys()]):
        msg = "config.json contains an undefined key."
        msg += f"Allowed keys are:\n{CONFIG_KEYS}"
        misconf = True
    if misconf:
        raise KeyError(msg)
    print(f"{timestamp()} - Config loaded")
    return config


def load_secrets():
    dev_secrets_path = join(HERE, SECRETS_FILENAME)
    if exists(dev_secrets_path):
        from json import load

        with open(dev_secrets_path, "r") as f:
            secrets = load(f)
    else:
        try:
            secrets = {v: environ[v] for v in SECRET_ENV_VARS}
        except KeyError as ke:
            print(f"{ke} environment variable must be defined.", file=stderr)
            exit(78)
    print(f"{timestamp()} - Secrets initialized")
    return secrets

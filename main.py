from datetime import datetime as dt
from github_reporter.github_reporter import GithubReporter
from google.cloud import error_reporting
from json import load
from os import environ
from os.path import abspath, dirname, exists, join
from sys import exit, stderr
from traceback import print_exc

# TODO: tidy up history
# TODO: Link back to index from report page. Stats on index page??
# TODO: move to PUL Github
# TODO: Make HTML responsive. Much more likely to be reading on phone.
# TODO: atom
# TODO: post to Slack: https://slack.dev/python-slackclient/basic_usage.html#sending-a-message
# TODO: implement a method for deleting (from index and pages)

CONFIG_FILENAME = 'config.json'
CONFIG_KEYS = ('base_page_title','github_repo_name','branch','github_org','timezone')
SECRET_ENV_VARS = ('GITHUB_TOKEN','GITHUB_ORGANIZATION')
SECRETS_FILENAME = 'secrets.json'
HERE = abspath(dirname(__file__))

def load_config():
    config_path = join(HERE, CONFIG_FILENAME)
    with open(config_path, 'r') as f:
        config = load(f)
    misconf = False
    msg = ''
    if not all([key in config for key in CONFIG_KEYS]):
        msg = f'{CONFIG_KEYS} must all be defined in config.json.'
        misconf = True
    if any([key not in CONFIG_KEYS for key in config.keys()]):
        msg = 'config.json contains an undefined key.'
        msg += f'Allowed keys are:\n{CONFIG_KEYS}'
        misconf = True
    if misconf:
        try:
            raise KeyError(msg)
        except KeyError:
            print_exc()
            exit(78)
    print(f'{dt.now().isoformat()} - Config loaded')
    return config

def load_secrets():
    dev_secrets_path = join(HERE, SECRETS_FILENAME)
    if exists(dev_secrets_path):
        with open(dev_secrets_path, 'r') as f:
            secrets = load(f)
    else:
        try:
            secrets = { v : environ[v] for v in SECRET_ENV_VARS }
        except KeyError as ke:
            print(f'{ke} environment variable must be defined.', file=stderr)
            exit(78)
    print(f'{dt.now().isoformat()} - Secrets initialized')
    return secrets

def main(event=None, context=None):
    is_google_run = event.get('is_google_run', True)
    dump_to_stdout = event.get('dump_to_stdout', False)
    secrets = load_secrets()
    config = load_config()
    try:
        if is_google_run:
            print(f'{dt.now().isoformat()} - Google called me')
        if dump_to_stdout:
            print(f'{dt.now().isoformat()} - Local run, will dump JSON to stdout')
        gh_reporter = GithubReporter(secrets, config, dump_to_stdout)
        commit_success = gh_reporter.run_report()
        print(f'{dt.now().isoformat()} - Commit success: {commit_success}')
        return 0
    except Exception:
        if is_google_run:
            erc = error_reporting.Client()
            erc.report_exception()
            return 1
        else:
            raise

if __name__ == '__main__':
    main(event={'is_google_run':False, 'dump_to_stdout':True})

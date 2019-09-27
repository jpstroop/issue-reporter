from json import dump, load
from github_reporter import IssueReporter
from os import environ
from os.path import abspath, dirname, exists, join
from sys import exit, stderr
import requests_cache

# TODO: grouping
# TODO: set 'since' date dynamically
# TODO: save out data as json w/ date-based name
# TODO: explore delegation patterns, e.g.:
#     class Event():
#         def __init__(self, event):
#             self.actor_name = event.actor.name
#             self.created_at = event.created_at
# ...seems lame
# TODO: Save HTML (index and pages), either w/ templating or javascript

SECRETS_FILENAME = 'secrets.json'
ENV_VARS = ('GITHUB_TOKEN','GITHUB_ORGANIZATION')

def main():
    requests_cache.install_cache('github_reporter', expire_after=300)
    config = _init_config()
    reporter = IssueReporter(config['GITHUB_TOKEN'], config['GITHUB_ORGANIZATION'])
    date = '2019-09-26T00:00:00'
    issue_report = reporter.issues_updated_since(date)
    with open('tmp/sample.json', 'w') as f:
        dump(issue_report, f, indent=2, ensure_ascii=False)

def _init_config():
    dev_config_path = join(abspath(dirname(__file__)), SECRETS_FILENAME)
    if exists(dev_config_path):
        with open(dev_config_path, 'r') as f:
            config = load(f)
    else:
        try:
            config = { v : environ[v] for v in ENV_VARS }
        except KeyError as ke:
            print(f'{ke} environment variable must be defined.', file=stderr)
            exit(78)
    return config


if __name__ == '__main__':
    main()

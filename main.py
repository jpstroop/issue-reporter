from datetime import datetime, timedelta
from github_reporter import IssueReporter
from json import dump, load
from os import environ
from os.path import abspath, dirname, exists, join
from sys import exit, stderr
import requests_cache

# TODO: explore delegation patterns, e.g.:
#     class Event():
#         def __init__(self, event):
#             self.actor_name = event.actor.name
#             self.created_at = event.created_at
# ...seems lame
# TODO: Save HTML (index and pages), either w/ templating or javascript

SECRETS_FILENAME = 'secrets.json'
ENV_VARS = ('GITHUB_TOKEN','GITHUB_ORGANIZATION')
HERE = abspath(dirname(__file__))

def main():
    requests_cache.install_cache('github_reporter', expire_after=300)
    config = _init_config()
    reporter = IssueReporter(config['GITHUB_TOKEN'], config['GITHUB_ORGANIZATION'])
    today = datetime.today().isoformat(timespec='seconds')
    yesterday = (datetime.today()-timedelta(days=1)).isoformat(timespec='seconds')
    issue_report = reporter.issues_updated_since(yesterday)
    issue_report['today'] = today
    issue_report['yesterday'] = yesterday
    issue_report.move_to_end('yesterday', last=False)
    issue_report.move_to_end('today', last=False)
    file_name = join(HERE, 'tmp', f'{today}.json')
    with open(file_name, 'w') as f:
        dump(issue_report, f, indent=2, ensure_ascii=False)

def _init_config():
    dev_config_path = join(HERE, SECRETS_FILENAME)
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

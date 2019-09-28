from datetime import datetime, timedelta
from github_reporter import IssueReporter
from json import dump, load
from os import environ
from os.path import abspath, dirname, exists, join
from sys import exit, stderr
import requests_cache

# TODO: write data to a data dir; config how many days we want to keep
# TODO: explore batch delegation patterns, e.g.:
#     class Event():
#         def __init__(self, event):
#             self.actor_name = event.actor.name
#             self.created_at = event.created_at
# ...seems lame
# TODO: Save HTML (index and pages), either w/ templating or javascript
# TODO: config file?

SECRETS_FILENAME = 'secrets.json'
ENV_VARS = ('GITHUB_TOKEN','GITHUB_ORGANIZATION')
HERE = abspath(dirname(__file__))

def main():
    requests_cache.install_cache('github_reporter', expire_after=300)
    secrets = _init_secrets()
    reporter = IssueReporter(secrets['GITHUB_TOKEN'], secrets['GITHUB_ORGANIZATION'])
    yesterday, today = _get_dates()
    issue_report = reporter.issues_updated_since(yesterday)
    issue_report['today'] = today
    issue_report['yesterday'] = yesterday
    issue_report.move_to_end('yesterday', last=False)
    issue_report.move_to_end('today', last=False)
    file_name = join(HERE, 'tmp', f'{today}.json')
    with open(file_name, 'w') as f:
        dump(issue_report, f, indent=2, ensure_ascii=False)

def _get_dates():
    today_dt = datetime.today()
    today = today_dt.isoformat(timespec='seconds')
    yesterday = (today_dt-timedelta(days=1)).isoformat(timespec='seconds')
    return (yesterday, today)

def _init_secrets():
    dev_secrets_path = join(HERE, SECRETS_FILENAME)
    if exists(dev_secrets_path):
        with open(dev_secrets_path, 'r') as f:
            secrets = load(f)
    else:
        try:
            secrets = { v : environ[v] for v in ENV_VARS }
        except KeyError as ke:
            print(f'{ke} environment variable must be defined.', file=stderr)
            exit(78)
    return secrets


if __name__ == '__main__':
    main()

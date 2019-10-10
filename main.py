from datetime import datetime
from github_reporter.github_reporter import GithubReporter
from google.cloud import error_reporting
from json import load
from os import environ
from os.path import abspath, dirname, exists, join
from sys import exit, stderr

# TODO: No email. Set a commit message that includes the link to the report.
#   Then anyone who wants a notification can just watch the repo.
# TODO: Index file. Easier to draw with javascript.
#   * Get a JSON file w/ HTTP (default to '{}')
#   * Update it
#   * Commit it back
# TODO: explore batch delegation patterns, e.g.
#     class Event():
#         def __init__(self, event):
#             self.actor_name = event.actor.name
#             self.created_at = event.created_at
# ...seems lame. See: https://www.michaelcho.me/article/method-delegation-in-python
# TODO: Link back to index from report page. Stats on index page??
# TODO: Make HTML responsive. Much more likely to be reading on phone.
# TODO: index (maybe javascript? Can we list dirs?)
# TODO: atom
# TODO: config file?
#  - base title for HTML
#  - number of days to keep (?)
#  - email addresses / names
#  - github org
#  - cache timing
#  - github repo and branch to push

SECRETS_FILENAME = 'secrets.json'
ENV_VARS = ('GITHUB_TOKEN','GITHUB_ORGANIZATION')

def load_secrets():
    dev_secrets_path = join(abspath(dirname(__file__)), SECRETS_FILENAME)
    if exists(dev_secrets_path):
        with open(dev_secrets_path, 'r') as f:
            secrets = load(f)
    else:
        try:
            secrets = { v : environ[v] for v in ENV_VARS }
            print(f'{datetime.now().isoformat()} - Secrets initialized')
        except KeyError as ke:
            print(f'{ke} environment variable must be defined.', file=stderr)
            exit(78)
    return secrets

def main(event=None, context=None):
    is_google_run = event.get('is_google_run', True)
    secrets = load_secrets()
    try:
        if is_google_run:
            print(f'{datetime.now().isoformat()} - Google called me!')
        gh_reporter = GithubReporter(secrets)
        commit_success = gh_reporter.run_report()
        print(f'{datetime.now().isoformat()} - Commit success: {commit_success}')
        return 0
    except Exception:
        if is_google_run:
            erc = error_reporting.Client()
            erc.report_exception()
            return 1
        else:
            raise

if __name__ == '__main__':
    main(event={'is_google_run':False})

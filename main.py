from datetime import datetime, timedelta
from github_reporter import IssueReporter
from github_reporter import HTMLReportRenderer
from json import dump, load
from os import environ
from os.path import abspath, dirname, exists, join
from sys import exit, stderr
import requests_cache

# TODO: write data to a data dir; config how many days we want to keep
#  - use UserList API to make a list-like object:
#        https://subscription.packtpub.com/book/application_development/9781788294874/4/ch04lvl1sec53/implementing-userlist
# TODO: explore batch delegation patterns, e.g.
#     class Event():
#         def __init__(self, event):
#             self.actor_name = event.actor.name
#             self.created_at = event.created_at
# ...seems lame. See: https://www.michaelcho.me/article/method-delegation-in-python
# TODO: push to github: https://stackoverflow.com/a/39627647/714478
# TODO: config file?
#  - base title for HTML
#  - number of days to keep
#  - email addresses / names
#  - github org
#  - cache timing
#  - github repo and branch to push

SECRETS_FILENAME = 'secrets.json'
ENV_VARS = ('GITHUB_TOKEN','GITHUB_ORGANIZATION')
HERE = abspath(dirname(__file__))

def main():
    requests_cache.install_cache('github_reporter', expire_after=300)
    secrets = init_secrets()
    reporter = IssueReporter(secrets['GITHUB_TOKEN'], secrets['GITHUB_ORGANIZATION'])
    yesterday, today = get_dates()
    issue_report = reporter.issues_updated_since(yesterday)

    ### TODO: add these to the issue report class? Would need to pass though
    ### issue reporter
    issue_report['today'] = today
    issue_report['yesterday'] = yesterday
    issue_report.move_to_end('yesterday', last=False)
    issue_report.move_to_end('today', last=False)
    ###

    serialize_report(issue_report)

def serialize_report(issue_report):
    json_path = render_as_json(issue_report)
    html_path = render_as_html(issue_report, 'issue_report_page.html.mako')
    return (json_path, html_path)

def commit_and_push():
    ## How? will the Cloud Function runtime have what we need (e.g. origin
    ## remotes?) Can we shell out if PyGithub doesn't push? See:
    ## https://stackoverflow.com/a/39627647/714478
    ## Seems like the cloud function will need a way to auth with github? Or is
    ## the API key enough?.
    ## Or, is there something we can do with basic auth over HTTP if we shell
    ## out? Looks like yes: https://stackoverflow.com/a/10054470/714478
    pass

def render_as_json(issue_report):
    file_name = f'{issue_report["today"].split("T")[0]}.json'
    file_path = join(HERE, 'docs', 'data', file_name)
    with open(file_path, 'w') as f:
        dump(issue_report, f, indent=2, ensure_ascii=False)
    return file_path

def render_as_html(issue_report, template):
    renderer = HTMLReportRenderer()
    file_name = f'{issue_report["today"].split("T")[0]}.html'
    file_path = join(HERE, 'docs', 'reports', file_name)
    with open(file_path, 'w') as f:
        f.write(renderer.render(template, r=issue_report))
    return file_path

def get_dates():
    today_dt = datetime.today()
    today = today_dt.isoformat(timespec='seconds')
    yesterday = (today_dt-timedelta(days=1)).isoformat(timespec='seconds')
    return (yesterday, today)

def init_secrets():
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

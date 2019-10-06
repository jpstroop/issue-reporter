from datetime import datetime, timedelta
from github_reporter import IssueReporter
from github_reporter import GithubCommitter
from github_reporter import HTMLReportRenderer
from json import dump, load
from os import environ, makedirs, sep, walk
from os.path import abspath, dirname, exists, join
from sys import exit, stderr
import requests_cache

# TODO: explore batch delegation patterns, e.g.
#     class Event():
#         def __init__(self, event):
#             self.actor_name = event.actor.name
#             self.created_at = event.created_at
# ...seems lame. See: https://www.michaelcho.me/article/method-delegation-in-python
# TODO: Link back to index from report page. Stats on index page??
# TODO: wrap all of the stuff not in main in a class. main() could even go in
#  the class and then be aliased (if main is static) or instantiate the class
#  and then call whatever it needs to call. main.py is curently not very DRY,
#  and all of these functions and HERE are getting annoying.
# TODO: Make HTML responsive. Much more likely to be reading on phone.
# TODO: Delete files after they are committed to the remote; otherwise the local
#  copy of the repo is in conflict and pushing updates is a pain.
# TODO: config file?
#  - base title for HTML
#  - number of days to keep (?)
#  - email addresses / names
#  - github org
#  - cache timing
#  - github repo and branch to push

SECRETS_FILENAME = 'secrets.json'
ENV_VARS = ('GITHUB_TOKEN','GITHUB_ORGANIZATION')
HERE = abspath(dirname(__file__))

def main(event=None, context=None):
    requests_cache.install_cache('github_reporter', expire_after=300)
    secrets = init_secrets()

    reporter = IssueReporter(secrets['GITHUB_TOKEN'], secrets['GITHUB_ORGANIZATION'])
    yesterday, today = get_dates()
    issue_report = reporter.issues_updated_since(yesterday)

    issue_report['today'] = today
    issue_report['yesterday'] = yesterday
    issue_report.move_to_end('yesterday', last=False)
    issue_report.move_to_end('today', last=False)

    file_paths = serialize_report(issue_report)
    committer = GithubCommitter(secrets['GITHUB_TOKEN'], HERE)
    message = f'reports for {today.split("T")[0]}'
    committer.commit(file_paths, message)
    return 0

def make_date_dirs(iso_datetime):
    date_dirs = iso_datetime.split("T")[0].split('-')
    dir = join(HERE, 'docs', 'reports', *date_dirs)
    makedirs(dir, exist_ok=True)
    return dir

def serialize_report(issue_report):
    json_path = render_as_json(issue_report)
    html_path = render_as_html(issue_report, 'issue_report_page.html.mako')
    index_path = make_index()
    return (json_path, html_path, index_path)

def render_as_json(issue_report):
    html_dir = make_date_dirs(issue_report["today"])
    dirs = html_dir.split(sep)
    file_name = f'{dirs.pop()}.json'
    file_path = f'{sep}{join(*dirs, file_name)}'
    with open(file_path, 'w') as f:
        dump(issue_report, f, indent=2, ensure_ascii=False)
    return file_path

def render_as_html(issue_report, template):
    renderer = HTMLReportRenderer()
    dir = make_date_dirs(issue_report["today"])
    file_path = join(dir, 'index.html')
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

def make_index():
    base = join(HERE, 'docs')
    index_files = []
    for root, _, files in walk(base):
        for name in filter(lambda f: f.endswith('index.html'), files):
            index_files.append(join(root, name).split(base)[1][1:])
    index_files.pop(0)
    renderer = HTMLReportRenderer()
    file_path = join(base, 'index.html')
    with open(file_path, 'w') as f:
        f.write(renderer.render('site_index.html.mako', index_files=index_files))
    return file_path

if __name__ == '__main__':
    main()

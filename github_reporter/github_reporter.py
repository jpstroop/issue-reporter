from contextlib import contextmanager
from datetime import datetime, timedelta
from github_reporter.github_committer import GithubCommitter
from github_reporter.html_report_renderer import HTMLReportRenderer
from github_reporter.issue_reporter import IssueReporter
from io import StringIO
from json import dumps
from os import sep
from os.path import join
from pytz import timezone
from requests import get
import requests_cache as rc

class GithubReporter():
    def __init__(self, secrets, config):
        rc.install_cache('ghr', backend='memory', expire_after=300)
        self.yesterday_iso, self.today_iso = self.get_dates(config['timezone'])
        self.secrets = secrets
        self.config = config
        # memoized vars
        self._report_path = None
        self._html_path = None
        self._json_path = None
        self._index_json_path = None
        self._issue_report = None

    @property
    def report_path(self):
        # returns a str representing the path where we'll ultimately want this
        # in the repo, without /index.html or .json, i.e.
        # docs/reports/YYYY/MM/DD
        if self._report_path is None:
            ymd = self.today_iso.split("T")[0].split('-')
            self._report_path = join('docs', 'reports', *ymd)
        return self._report_path

    @property
    def index_json_path(self):
        if self._index_json_path is None:
            self._index_json_path = join('docs', 'index.json')
            print(f'{datetime.now().isoformat()} - Index JSON path: {self._index_json_path}')
        return self._index_json_path

    @property
    def html_path(self):
        if self._html_path is None:
            self._html_path = join(self.report_path, 'index.html')
            print(f'{datetime.now().isoformat()} - HTML path: {self._html_path}')
        return self._html_path

    @property
    def json_path(self):
        if self._json_path is None:
            self._json_path = f'{self.report_path}.json'
            print(f'{datetime.now().isoformat()} - JSON path: {self._json_path}')
        return self._json_path

    @property
    def issue_report(self):
        if self._issue_report is None:
            token = self.secrets['GITHUB_TOKEN']
            org = self.secrets['GITHUB_ORGANIZATION']
            r = IssueReporter(token, org)
            self._issue_report = r.issues_updated_since(self.yesterday_iso)
            self._add_dates_to_report()
            print(f'{datetime.now().isoformat()} - Report ran successfully')
        return self._issue_report

    def _add_dates_to_report(self):
        self.issue_report['today'] = self.today_iso
        self.issue_report['yesterday'] = self.yesterday_iso
        self.issue_report.move_to_end('yesterday', last=False)
        self.issue_report.move_to_end('today', last=False)
        print(f'{datetime.now().isoformat()} - Dates added to report')

    def get_dates(self, tz):
        today_dt = datetime.now(timezone(tz)).replace(tzinfo=None)
        today = today_dt.isoformat(timespec='seconds')
        yesterday = (today_dt-timedelta(days=1)).isoformat(timespec='seconds')
        print(f'{datetime.now().isoformat()} - Today: {today}')
        print(f'{datetime.now().isoformat()} - Yesterday: {yesterday}')
        return (yesterday, today)

    @contextmanager
    def report_strings(self):
        json_string = StringIO(self.render_as_json())
        html_string = StringIO(self.render_as_html())
        index_string = StringIO(self.updated_index())
        yield json_string, html_string, index_string
        json_string.close()
        html_string.close()
        index_string.close()

    def render_as_json(self):
        json = dumps(self.issue_report, indent=2, ensure_ascii=False)
        print(f'{datetime.now().isoformat()} - JSON serialized successfully')
        return json

    def render_as_html(self):
        renderer = HTMLReportRenderer()
        template = 'issue_report_page.html.mako'
        html = renderer.render(template, r=self.issue_report)
        print(f'{datetime.now().isoformat()} - HTML serialized successfully')
        return html

    def updated_index(self):
        index = self.get_current_index()
        date = self.today_iso.split('T')[0]
        index = list(filter(lambda e: e['date'] != date, index))
        entry = {
            'date' : date,
            'run_start' : self.today_iso,
            'html' : sep.join(self.html_path.split(sep)[1:]), # removes docs/
            'json' : sep.join(self.json_path.split(sep)[1:])  # removes docs/
        }
        index.insert(0, entry)
        return dumps(index, indent=2, ensure_ascii=False)

    def get_current_index(self):
        org = self.config['github_org']
        repo = self.config['github_repo_name']
        url = f'https://{org}.github.io/{repo}/index.json'
        with rc.disabled():
            print(f'{datetime.now().isoformat()} - Getting {url} for updating')
            headers = { 'cache-control' : 'no-store'} # not sure if this makes a differnce;
            index_json = get(url, headers=headers).json()
        return index_json

    def run_report(self):
        with self.report_strings() as (json_str, html_str, index_str):
            repo = self.config['github_repo_name']
            committer = GithubCommitter(self.secrets['GITHUB_TOKEN'], repo)
            date = self.today_iso.split("T")[0]
            message = f'[automated commit] reports for {date}'
            print(f'{datetime.now().isoformat()} - Committing {message}')
            path_data_pairs = (
                (self.json_path, json_str),
                (self.html_path, html_str),
                (self.index_json_path, index_str)
            )
            branch = self.config['branch']
            commit_success = committer.commit(path_data_pairs, message, branch)
        return commit_success

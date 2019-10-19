from cached_property import cached_property
from contextlib import contextmanager
from datetime import datetime, timedelta
from github_reporter.data.issue_report import IssueReport
from github_reporter.github_committer import GithubCommitter
from io import StringIO
from json import dumps
from os import sep
from os.path import join
from pytz import timezone
from requests import get
import requests_cache as rc

class GithubReporter():
    def __init__(self, secrets, config, dump_to_stdout=False):
        rc.install_cache('ghr', backend='memory', expire_after=300)
        self.dump_to_stdout = dump_to_stdout
        self.yesterday_iso, self.today_iso = self.get_dates(config['timezone'])
        self.secrets = secrets
        self.config = config
        # memoized vars
        self._index_json_path = None
        self._issue_report = None

    @cached_property
    def issue_report(self):
        token = self.secrets['GITHUB_TOKEN']
        org = self.secrets['GITHUB_ORGANIZATION']
        self._issue_report = IssueReport(token, org, self.yesterday_iso, self.today_iso)
        return self._issue_report

    def get_dates(self, tz):
        today_dt = datetime.now(timezone(tz)).replace(tzinfo=None)
        today = today_dt.isoformat(timespec='seconds')
        yesterday = (today_dt-timedelta(days=1)).isoformat(timespec='seconds')
        print(f'{datetime.now().isoformat()} - Today: {today}')
        print(f'{datetime.now().isoformat()} - Yesterday: {yesterday}')
        return (yesterday, today)

    @contextmanager
    def report_strings(self):
        json_string = StringIO(self.issue_report.as_json())
        html_string = StringIO(self.issue_report.as_html())
        index_string = StringIO(self.updated_index())
        yield json_string, html_string, index_string
        json_string.close()
        html_string.close()
        index_string.close()

    @cached_property
    def index_json_path(self):
        self._index_json_path = join('docs', 'index.json')
        print(f'{datetime.now().isoformat()} - Index JSON path: {self._index_json_path}')
        return self._index_json_path

    def updated_index(self):
        index = self.get_current_index()
        date = self.today_iso.split('T')[0]
        index = list(filter(lambda e: e['date'] != date, index))
        entry = {
            'date' : date,
            'meta' : self.issue_report.grouped_issues['__meta__'],
            'run_start' : self.today_iso,
            'html' : f'{sep.join(self.issue_report.html_path.split(sep)[1:-1])}{sep}', # removes docs/ and index.html
            'json' : sep.join(self.issue_report.json_path.split(sep)[1:])  # removes docs/
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
            if self.dump_to_stdout:
                print(json_str.read())
                commit_success = True
            else:
                repo = self.config['github_repo_name']
                committer = GithubCommitter(self.secrets['GITHUB_TOKEN'], repo)
                date = self.today_iso.split("T")[0]
                message = f'[automated commit] reports for {date}'
                print(f'{datetime.now().isoformat()} - Committing {message}')
                path_data_pairs = (
                    (self.issue_report.json_path, json_str),
                    (self.issue_report.html_path, html_str),
                    (self.index_json_path, index_str)
                )
                branch = self.config['branch']
                commit_success = committer.commit(path_data_pairs, message, branch)
        return commit_success

from contextlib import contextmanager
from datetime import datetime, timedelta
from github_reporter.github_committer import GithubCommitter
from github_reporter.html_report_renderer import HTMLReportRenderer
from github_reporter.issue_reporter import IssueReporter
from io import StringIO
from json import dumps
from os.path import join
from pytz import timezone
import requests_cache

class GithubReporter():
    def __init__(self, secrets, config={}):
        requests_cache.install_cache('ghr', backend='memory', expire_after=300)
        self.yesterday_iso, self.today_iso = GithubReporter.get_dates()
        self.secrets = secrets
        self.config = config # TODO
        # memoized vars
        self._report_path = None
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

    @staticmethod
    def get_dates():
        today_dt = datetime.now(timezone('America/New_York')).replace(tzinfo=None)
        today = today_dt.isoformat(timespec='seconds')
        yesterday = (today_dt-timedelta(days=1)).isoformat(timespec='seconds')
        print(f'{datetime.now().isoformat()} - Today: {today}')
        print(f'{datetime.now().isoformat()} - Yesterday: {yesterday}')
        return (yesterday, today)

    @contextmanager
    def report_strings(self):
        json_string = StringIO(self.render_as_json())
        html_string = StringIO(self.render_as_html())
        yield json_string, html_string
        json_string.close()
        html_string.close()

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

    def run_report(self):
        with self.report_strings() as (json_str, html_str):
            json_path = f'{self.report_path}.json'
            print(f'{datetime.now().isoformat()} - JSON path: {json_path}')
            html_path = join(self.report_path, 'index.html')
            print(f'{datetime.now().isoformat()} - HTML path: {html_path}')

            committer = GithubCommitter(self.secrets['GITHUB_TOKEN'])
            date = self.today_iso.split("T")[0]
            message = f'[automated commit] reports for {date}'
            print(f'{datetime.now().isoformat()} - Committing {message}')
            path_data_pairs = (
                (json_path, json_str),
                (html_path, html_str),
            )
            commit_success = committer.commit(path_data_pairs, message)
        return commit_success

    def update_index(self):
        pass

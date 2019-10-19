from cached_property import cached_property
from collections import OrderedDict
from datetime import datetime as dt
from github import Github
from github_reporter.data import ReportJSONEncoder
from github_reporter.data.issue import Issue
from github_reporter.html_report_renderer import HTMLReportRenderer
from itertools import groupby
from json import dumps
from os.path import join

class IssueReport():
    def __init__(self, gh_token, gh_org, yesterday_iso, today_iso):
        #memoized properties:
        self._generic_report_path = None
        self._html_path = None
        self._json_path = None
        # the issues
        self.yesterday_iso = yesterday_iso
        self.today_iso = today_iso
        q = f'org:{gh_org} updated:>={self.yesterday_iso}'
        print(f'{dt.now().isoformat()} - Report started')
        paged_issues = [i for i in Github(gh_token).search_issues(query=q)]
        self.issues = [Issue(i, self.yesterday_iso) for i in paged_issues]
        self.grouped_issues = IssueReport.group_issues(self.issues)
        self.grouped_issues['__meta__'] = IssueReport.gather_stats(self.issues)
        self.grouped_issues['__meta__']['today'] = self.today_iso
        self.grouped_issues['__meta__']['yesterday'] = self.yesterday_iso
        print(f'{dt.now().isoformat()} - Report ran successfully')

    def as_json(self):
        json = dumps(self.grouped_issues, indent=2, ensure_ascii=False, cls=ReportJSONEncoder)
        print(f'{dt.now().isoformat()} - JSON serialized successfully')
        return json

    def as_html(self):
        renderer = HTMLReportRenderer()
        template = 'issue_report_page.html.mako'
        html = renderer.render(template, r=self.grouped_issues)
        print(f'{dt.now().isoformat()} - HTML serialized successfully')
        return html

    @cached_property
    def generic_report_path(self):
        # returns a str representing the path where we'll ultimately want this
        # in the repo, without /index.html or .json, i.e.
        # docs/reports/YYYY/MM/DD
        ymd = self.today_iso.split("T")[0].split('-')
        self._generic_report_path = join('docs', 'reports', *ymd)
        return self._generic_report_path

    @cached_property
    def html_path(self):
        self._html_path = join(self.generic_report_path, 'index.html')
        print(f'{dt.now().isoformat()} - HTML path: {self._html_path}')
        return self._html_path

    @cached_property
    def json_path(self):
        self._json_path = f'{self.generic_report_path}.json'
        print(f'{dt.now().isoformat()} - JSON path: {self._json_path}')
        return self._json_path

    @staticmethod
    def group_issues(issues):
        print(f'{dt.now().isoformat()} - Grouping by repo started')
        groups = OrderedDict()
        issues.sort(key=lambda i: (i.repository_name, i.updated_at))
        for repo, issues in groupby(issues, lambda i: i.repository_name):
            groups[repo] = list(issues)
            # we need to use the issues multiple times when  we serialize
            # hence the `list(_grouper)` cast.
        return groups

    @staticmethod
    def gather_stats(issues):
        groups = { 'issue_count' : len(issues) }
        issues.sort(key=lambda r: r.action)
        for action, issues in groupby(issues, lambda r: r.action):
            groups[f'{action}_count'] = len(list(issues))
        return groups

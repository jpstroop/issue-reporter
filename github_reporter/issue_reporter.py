from collections import OrderedDict
from datetime import datetime as dt
from github import Github
from github_reporter.data_classes.issue import Issue
from itertools import groupby

class IssueReporter():
    def __init__(self, github_token, github_organization):
        self._github_organization = github_organization
        self.github = Github(github_token)

    def issues_updated_since(self, date):
        q = f'org:{self._github_organization} updated:>={date}'
        print(f'{dt.now().isoformat()} - Report started')
        paged_issues = [i for i in self.github.search_issues(query=q)]
        paged_issues.sort(key=lambda i: (i.repository.name, i.updated_at))
        reports = [Issue(i, date) for i in paged_issues]
        stats = IssueReporter.stats(reports)
        # TODO: we need to stop passing around dicts, and work with objects.
        # Implement JSONEncoder.
        reports = list(map(dict, reports))
        return (IssueReporter.group_reports(reports), stats)

    @staticmethod
    def group_reports(report_list, key='repository_name'):
        print(f'{dt.now().isoformat()} - Grouping by repo started')
        groups = OrderedDict()
        for repo, issues in groupby(report_list, lambda o: o[key]):
            issues = list(issues)
            [d.pop(key) for d in issues]
            groups[repo] = issues
        return groups

    @staticmethod
    def stats(reports):
        groups = { 'issue_count' : len(reports) }
        reports.sort(key=lambda r: r.action)
        for action, issues in groupby(reports, lambda r: r.action):
            groups[f'{action}_count'] = len(list(issues))
        return groups

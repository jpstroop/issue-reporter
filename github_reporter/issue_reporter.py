from collections import OrderedDict
from datetime import datetime as dt
from github import Github
from github_reporter.data_classes.issue import Issue
from itertools import groupby

class IssueReporter():
    def __init__(self, github_token, github_organization):
        self._github_organization = github_organization
        self.github = Github(github_token)

    def issues_updated_since(self, iso_date_str):
        q = f'org:{self._github_organization} updated:>={iso_date_str}'
        print(f'{dt.now().isoformat()} - Report started')
        paged_issues = [i for i in self.github.search_issues(query=q)]
        issues = [Issue(i, iso_date_str) for i in paged_issues]
        # NB. `issues` needs to be a list (as opposed to generator) for when we
        # sort/group below
        grouped_issues = IssueReporter.group_issues(issues)
        grouped_issues['__meta__'] = IssueReporter.stats(issues)
        return grouped_issues #OrderedDict

    @staticmethod
    def group_issues(issues, key='repository_name'):
        print(f'{dt.now().isoformat()} - Grouping by repo started')
        groups = OrderedDict()
        issues.sort(key=lambda i: (i.repository_name, i.updated_at))
        for repo, issues in groupby(issues, lambda i: i.repository_name):
            groups[repo] = list(issues)
            # we need to use the issues multiple times when  we serialize
            # hence the `list(_grouper)` cast.
        return groups

    @staticmethod
    def stats(issues):
        groups = { 'issue_count' : len(issues) }
        issues.sort(key=lambda r: r.action)
        for action, issues in groupby(issues, lambda r: r.action):
            groups[f'{action}_count'] = len(list(issues))
        return groups

from datetime import datetime
from github import Github
from json import dumps
from json import load
from os import environ
from os.path import abspath
from os.path import dirname
from os.path import exists
from os.path import join
from sys import exit
from sys import stderr

SECRETS_FILENAME = 'secrets.json'
ENV_VARS = ('GITHUB_TOKEN','GITHUB_ORGANIZATION')

def main():
    config = _init_config()
    reporter = IssueReporter(config['GITHUB_TOKEN'], config['GITHUB_ORGANIZATION'])
    # https://pygithub.readthedocs.io/en/latest/github.html#github.MainClass.Github.search_issues
    date = '2019-09-25T00:00:00'
    issue_report = reporter.issues_updated_since(date)
    for i in issue_report:
        print(dumps(i, indent=2))

    # TODO: make a dict/JSON structure that contains everything we need to make
    # HTML formatting as easy as possible

def _init_config():
    dev_config_path = join(abspath(dirname(__file__)), SECRETS_FILENAME)
    if exists(dev_config_path):
        with open(dev_config_path, 'r') as f:
            config = load(f)
    else:
        try:
            config = { v : environ[v] for v in ENV_VARS }
        except KeyError as ke:
            print(f'{ke} environment variable must be defined.', file=stderr)
            exit(78)
    return config


class IssueReporter():
    def __init__(self, github_token, github_organization):
        self._github_token = github_token
        self._github_organization = github_organization
        self._github = None
        self._all_repos = None

    @property
    def github(self):
        if self._github is None:
            self._github = Github(self._github_token)
        return self._github

    @property
    def all_repos(self):
        if self._all_repos is None:
            # TODO: https://pygithub.readthedocs.io/en/latest/github_objects/Organization.html#github.Organization.Organization.get_repos
            org = self.github.get_organization(self._github_organization)
            paged_repos = org.get_repos(type='all', sort='full_name')
            self._all_repos = [r for r in paged_repos]
        return self._all_repos

    def issues_updated_since(self, date):
        '''Returns a list of github.Issue.Issue
        https://pygithub.readthedocs.io/en/latest/github_objects/Issue.html#github.Issue.Issue
        '''
        q = f'org:{self._github_organization} updated:>={date}'
        paged_issues = [i for i in self.github.search_issues(query=q)]
        paged_issues.sort(key=lambda i: (i.repository.name, i.updated_at))
        reports = [IssueReport(i, date) for i in paged_issues]
        return [dict(r) for r in reports]
        # TODO: these need to be dicts at some point, maybe??
        # return GroupedIssueReport(reports).asdict()

# TODO: group reports by repository_name
# Dump to a file as JSON
# Move classes into a module

    def publish_report(dir):
        pass

class GroupedIssueReport():
    def __init__(self, issue_reports):
        self.issue_reports = issue_reports
    # TODO: holds logic for grouping issues into a dict by repository, i.e.:
    # repo_name : [IssueReport(), IssueReport(), ...]

    def asdict(self):
        # TODO: grouping, and then something more idiomatic that allows us
        # to call dict() https://stackoverflow.com/a/35282286
        return self.issue_reports

class IssueReport():
    def __init__(self, issue, date):
        self.date = datetime.fromisoformat(date)
        self.issue = issue
        self.created_at = issue.created_at
        self.html_url = issue.html_url
        self.number = issue.number
        self.repository_html_url = issue.repository.html_url
        self.repository_name = issue.repository.name
        self.state = issue.state
        self.title = issue.title
        self.user_name = issue.user.name

    def keys(self):
        return ('created_at','html_url','number','pull_request_html_url',
            'repository_html_url','repository_name','state','title','user_name',
            'comments','events')

    def __getitem__(self, key):
        vals = (str(self.created_at), self.html_url, self.number,
            self.pull_request_html_url, self.repository_html_url,
            self.repository_name, self.state, self.title, self.user_name,
            self.comments, self.events)
        return dict(zip(self.keys(), vals))[key]

    @property
    def comments(self):
        comments = [Comment(c) for c in self.issue.get_comments(since=self.date)]
        return [dict(c) for c in comments]

    @property
    def events(self):

        def event_filter(e):
            ok_types = ('closed', 'merged', 'reopened')
            return e.created_at >= self.date and event.event in ok_types

        events = [Event(e) for e in self.issue.get_events()]
        return [dict(e) for e in filter(event_filter, events)]

    @property
    def pull_request_html_url(self):
        if self.issue.pull_request:
            return self.issue.pull_request.html_url

class Event():
    def __init__(self, event):
        self.actor_name = event.actor.name
        self.created_at = event.created_at
        self.type = event.event

    def keys(self):
        return ('actor_name', 'created_at', 'type')

    def __getitem__(self, key):
        vals = (self.actor_name, str(self.created_at), self.type)
        return dict(zip(self.keys(), vals))[key]

class Comment():
    def __init__(self, comment):
        self.body = comment.body
        self.html_url = comment.html_url
        self.updated_at = comment.updated_at
        self.user_name = comment.user.name

    def keys(self):
        return ('user_name','updated_at','html_url','body')

    def __getitem__(self, key):
        vals = (self.user_name, str(self.updated_at), self.html_url, self.body)
        return dict(zip(self.keys(), vals))[key]

if __name__ == '__main__':
    main()

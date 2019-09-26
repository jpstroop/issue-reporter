from datetime import datetime
from github import Github

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
        # Returns a list of github.Issue.Issue(s)
        q = f'org:{self._github_organization} updated:>={date}'
        paged_issues = [i for i in self.github.search_issues(query=q)]
        paged_issues.sort(key=lambda i: (i.repository.name, i.updated_at))
        reports = [dict(IssueReport(i, date)) for i in paged_issues]
        return reports
        # return GroupedIssueReport(reports)

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

        def issue_event_filter(e):
            # Note that this filter works on github.IssueEvent.IssueEvent(s)
            # (not our Events)
            ok_types = ('closed', 'merged', 'reopened') # config option?
            return e.created_at >= self.date and e.event in ok_types

        events = [Event(e) for e in filter(issue_event_filter, self.issue.get_events())]
        return [dict(e) for e in events]


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

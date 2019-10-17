from cached_property import cached_property
from datetime import datetime
from github_reporter import AbstractDataClass
from github_reporter.comment import Comment
from github_reporter.event import Event

class IssueReport(AbstractDataClass):
    def __init__(self, issue, date):
        super().__init__()
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
        if not self.user_name:
            self.user_name = issue.user.login
        self.pr_html_url = None
        if issue.pull_request:
            self.pr_html_url = issue.pull_request.html_url
        self._events = None
        self._comments = None
        self._action = None

    @property
    def _vals(self):
        return (self.created_at.isoformat(), self.html_url, self.number,
            self.pull_request_html_url, self.repository_html_url,
            self.repository_name, self.state, self.title, self.user_name,
            self.comments, self.events, self.pr_html_url, self.action)

    def keys(self):
        return ('created_at','html_url','number','pull_request_html_url',
            'repository_html_url','repository_name','state','title','user_name',
            'comments','events','pr_html_url', 'action')

    @cached_property
    def comments(self):
        cs = [Comment(c) for c in self.issue.get_comments(since=self.date)]
        self._comments = [dict(c) for c in cs]
        return self._comments

    @cached_property
    def events(self):
        filtr = lambda e: e.created_at >= self.date and e.event
        es = [Event(e) for e in filter(filtr, self.issue.get_events())]
        self._events = [dict(e) for e in es]
        return self._events

    @property
    def pull_request_html_url(self):
        if self.issue.pull_request:
            return self.issue.pull_request.html_url

    @cached_property
    def action(self):
        if self.created_at >= self.date:
            self._action = 'created'
        elif self.state == 'closed':
            self._action = 'closed'
        else:
            self._action = 'updated'
        return self._action

from datetime import datetime
from github_reporter import AbstractDataClass
from github_reporter.comment import Comment
from github_reporter.event import Event

class IssueReport(AbstractDataClass):
    def __init__(self, issue, date):
        super().__init__()
        self.date = datetime.fromisoformat(date)
        self.issue = issue
        self.created_at = issue.created_at.isoformat()
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

    @property
    def _vals(self):
        return (self.created_at, self.html_url, self.number,
            self.pull_request_html_url, self.repository_html_url,
            self.repository_name, self.state, self.title, self.user_name,
            self.comments, self.events, self.pr_html_url)

    def keys(self):
        return ('created_at','html_url','number','pull_request_html_url',
            'repository_html_url','repository_name','state','title','user_name',
            'comments','events','pr_html_url')

    @property
    def comments(self):
        comments = [Comment(c) for c in self.issue.get_comments(since=self.date)]
        return [dict(c) for c in comments]

    @property
    def events(self):

        def issue_event_filter(e):
            return e.created_at >= self.date and e.event

        events = [Event(e) for e in filter(issue_event_filter, self.issue.get_events())]
        return [dict(e) for e in events]

    @property
    def pull_request_html_url(self):
        if self.issue.pull_request:
            return self.issue.pull_request.html_url

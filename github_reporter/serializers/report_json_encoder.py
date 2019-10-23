from datetime import datetime
from github_reporter.data.comment import Comment
from github_reporter.data.event import Event
from github_reporter.data.issue import Issue
from json import JSONEncoder


class ReportJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, (Comment, Event, Issue)):
            return dict(obj)
        elif ReportJSONEncoder.is_iterable(obj):
            return list(obj)
        else:
            return JSONEncoder.default(self, obj)

    @staticmethod
    def is_iterable(obj):
        try:
            i = iter(obj)
        except TypeError:
            return False
        return True

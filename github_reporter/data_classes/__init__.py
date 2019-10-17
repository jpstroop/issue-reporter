from datetime import datetime
from github_reporter.data_classes.comment import Comment
from github_reporter.data_classes.event import Event
from github_reporter.data_classes.issue import Issue
from json import JSONEncoder

class ReportJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, (Comment, Event, Issue)):
            return dict(obj)
        elif ReportJSONEncoder.is_iterable(obj) or isinstance(obj, map):
            return list(obj)
        else:
            return JSONEncoder.default(self, obj)

    @staticmethod
    def is_iterable(obj):
        try:
            _ = iter(object)
        except TypeError:
            return False
        return True

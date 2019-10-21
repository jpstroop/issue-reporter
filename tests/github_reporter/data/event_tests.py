from github_reporter.data.event import Event
from unittest.mock import Mock

class EventTests():

# Mocking:
#   https://pygithub.readthedocs.io/en/latest/github_objects/IssueEvent.html

    def test_delegates_are_set(self, event_props):
        gh_event = Mock(**event_props)
        event = Event(gh_event)
        assert event.created_at == event_props['created_at']
        assert event.actor_name == event_props['actor.name']
        assert event.type == event_props['event']

    def test_cast_to_dict(self, event_props):
        gh_event = Mock(**event_props)
        event = Event(gh_event)
        expected = {
            'created_at' : event_props['created_at'],
            'actor_name' : event_props['actor.name'],
            'type' : event_props['event']
        }
        assert dict(event) == expected

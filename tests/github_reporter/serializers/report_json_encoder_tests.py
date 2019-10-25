from datetime import datetime
from github_reporter.data.event import Event
from github_reporter.serializers.report_json_encoder import ReportJSONEncoder
from json import dumps, loads
from pytest import raises
from unittest.mock import Mock

class ReportJSONEncoderTests():

    def test_it_handles_datetimes(self, faker):
        date = faker.date_time()
        d = { 'date' : date }
        encoded = dumps(d, cls=ReportJSONEncoder)
        expected = f'{{"date": "{date.isoformat()}"}}'
        assert encoded == expected

    def test_it_handles_iterables(self):
        d = { 'i' : range(5) }
        encoded = dumps(d, cls=ReportJSONEncoder)
        expected = '{"i": [0, 1, 2, 3, 4]}'
        assert encoded == expected

    def test_it_handle_events(self, event_props):
        gh_event = Mock(**event_props)
        event = Event(gh_event)
        encoded = dumps(event, cls=ReportJSONEncoder)
        decoded = loads(encoded)
        assert decoded['created_at'] == event_props['created_at'].isoformat()
        assert decoded['type'] == event_props['event']
        assert decoded['actor_name'] == event_props['actor.name']


    def test_raises_typeerrror(self):
        with raises(TypeError):
            dumps(Mock(cannot='serialize'), cls=ReportJSONEncoder)

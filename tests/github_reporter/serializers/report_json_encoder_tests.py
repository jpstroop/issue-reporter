from datetime import datetime
from github_reporter.serializers.report_json_encoder import ReportJSONEncoder
from json import dumps

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

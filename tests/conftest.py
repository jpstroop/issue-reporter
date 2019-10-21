
from faker import Faker
from faker.providers import date_time, internet, lorem, person
from custom_fakers import Provider as CustomProviders
from os.path import abspath, dirname
from pytest import fixture
from sys import path as pythonpath


# We need this so that we can find our application
project_dir = dirname(dirname(abspath(__file__)))
pythonpath.insert(0, project_dir)

# Fixture docs: https://docs.pytest.org/en/latest/fixture.html
# Faker docs: https://faker.readthedocs.io/en/stable/
# Faker providers: https://faker.readthedocs.io/en/stable/providers.html

@fixture(scope="session", autouse=True)
def faker():
    faker = Faker()
    faker.add_provider(CustomProviders)
    faker.add_provider(date_time)
    faker.add_provider(internet)
    faker.add_provider(lorem)
    faker.add_provider(person)
    return faker

@fixture(scope='function')
def event_props(faker):
    return {
        'created_at' : faker.date_time_between(start_date="-1d"),
        'event' : faker.event_type(),
        'actor.name' : faker.name()
    }

@fixture(scope='function')
def comment_props_with_username(faker):
    return {
        'body' : faker.paragraph(),
        'html_url' : faker.url(),
        'updated_at' : faker.date_time_between(start_date="-1d"),
        'user.name' : faker.name()
    }
@fixture(scope='function')
def comment_props_without_username(faker):
    return {
        'body' : faker.paragraph(),
        'html_url' : faker.url(),
        'updated_at' : faker.date_time_between(start_date="-1d"),
        'user.name' : None,
        'user.login' : faker.user_name()
    }

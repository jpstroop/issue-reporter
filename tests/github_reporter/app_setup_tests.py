from copy import deepcopy
from github_reporter.app_setup import CONFIG_KEYS, check_config, load_config, load_secrets
from pytest import raises

class AppSetupTests():

    def test_config_loads(self):
        load_config()

    def test_check_config_raises_keyerror_if_missing_key(self, faker):
        with raises(KeyError) as ke:
            keys = list(deepcopy(CONFIG_KEYS))
            keys.pop()
            fake_config = { k : faker.word() for k in keys }
            check_config(fake_config)
        assert "must all be defined" in str(ke.value)

    def test_check_config_raises_keyerror_if_extra_key(self, faker):
        with raises(KeyError) as ke:
            keys = list(deepcopy(CONFIG_KEYS))
            keys.append(faker.word())
            fake_config = { k : faker.word() for k in keys }
            check_config(fake_config)
        assert "contains an undefined key" in str(ke.value)

    def test_load_config_raises_keyerror_if_no_env_vars(self):
        # Note: this will fail if the secret environment variables are
        #   defined. Not a problem right now, but we could consider a skipif
        #   http://doc.pytest.org/en/latest/skipping.html#id1
        with raises(KeyError) as ke:
            load_secrets(allow_from_file=False)
        assert "environment variable must be defined" in str(ke.value)

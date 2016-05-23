"""
Tests for the configuration system
"""

import io
import json
import os.path
import unittest
import unittest.mock

import nose

from mcadminpanel.agent.config import Configuration
from mcadminpanel.agent.errors import ConfigurationError

class TestConfiguration(unittest.TestCase):
    """
    Tests for the configuration system
    """

    def setUp(self):
        self.user_home = os.path.expanduser('~')

    @unittest.mock.patch('builtins.open')
    def test_constr_default_path(self, fake_open):
        """
        Tests that the constructor uses a suitable default file path
        """

        fake_open.return_value = io.StringIO('{}')

        Configuration()

        fake_open.assert_called_with(
            os.path.join(self.user_home, 'mcadminpanel', 'config.json'), 'r'
        )

    @unittest.mock.patch('builtins.open')
    def test_file_option_exists(self, fake_open):
        """
        Tests that the values from the configuration file are loaded
        """

        options = {
            'test': 'value',
            'key': 'value',
        }

        fake_open.return_value = io.StringIO(
            json.dumps(options)
        )

        config = Configuration()

        for key, value in options.items():
            self.assertEqual(
                value,
                getattr(config, key),
                'Missing configuration value from file',
            )

    @unittest.mock.patch('builtins.open')
    def test_default_option_exists(self, fake_open):
        """
        Tests that the values from the defaults are used if not specified
        """

        fake_open.return_value = io.StringIO('{}')

        config = Configuration()

        for key, value in Configuration.DEFAULTS.items():
            self.assertEqual(
                value,
                getattr(config, key),
                'Missing configuration from defaults',
            )

    @unittest.mock.patch('builtins.open')
    def test_file_overrides_defaults(self, fake_open):
        """
        Tests that the file value override the defaults
        """

        fake_open.return_value = io.StringIO(
            json.dumps(
                {
                    'root': 'test',
                }
            )
        )

        config = Configuration()

        self.assertEqual(
            'test',
            config.root,
            'Root option was not overriden by file options',
        )

    @unittest.mock.patch('builtins.open')
    def test_deep_merge(self, fake_open):
        """
        Tests that we deep merge defaults into the resulting configuration
        """

        fake_open.return_value = io.StringIO(
            json.dumps(
                {
                    'logging': {
                        'level': 'debug',
                    },
                }
            )
        )

        config = Configuration()

        self.assertEqual(
            'debug',
            config.logging['level'],
            'Log level was not updated',
        )

        self.assertEqual(
            os.path.expanduser(os.path.join('~', 'mcadminpanel', 'agent.log')),
            config.logging['file'],
        )

    @unittest.mock.patch('builtins.open')
    def test_save_default_config(self, fake_open):
        """
        Tests that we can save a default configuration file
        """

        file_stream = io.StringIO()

        fake_open.return_value = fake_open
        fake_open.__enter__.return_value = file_stream

        Configuration.save_default_config('test.json')

        fake_open.assert_called_with('test.json', 'w')

        self.assertDictEqual(
            Configuration.DEFAULTS,
            json.loads(file_stream.getvalue()),
            'Default config did not contain the correct values',
        )

@unittest.mock.patch('builtins.open')
def test_constr_with_path(fake_open):
    """
    Tests that the constructor uses the correct given path
    """

    fake_open.return_value = io.StringIO('{}')

    Configuration('test_config.txt')

    fake_open.assert_called_with('test_config.txt', 'r')

@nose.tools.raises(ConfigurationError)
@unittest.mock.patch('builtins.open')
def test_constr_io_except(fake_open):
    """
    Tests that we properly handle an IO exception when opening the config
    """

    fake_open.side_effect = IOError

    Configuration()

@nose.tools.raises(ConfigurationError)
@unittest.mock.patch('builtins.open')
def test_constr_json_except(fake_open):
    """
    Tests that we properly handle JSON parse exceptions
    """

    fake_open.return_value = io.StringIO('{')

    Configuration()


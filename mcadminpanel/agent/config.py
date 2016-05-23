"""
MCAdminPanel Agent configuration management
"""

import copy
import json
import os.path

import mcadminpanel.agent.errors

# pylint: disable=too-few-public-methods
class Configuration(object):
    """
    MCAdminPanel configuration object for storing configuration options and
    managing their serialization and deserialization from the disk.
    """

    DEFAULT_CONFIG_FILE = os.path.expanduser(
        os.path.join('~', 'mcadminpanel', 'config.json')
    )

    DEFAULTS = {
        'root': os.path.expanduser(
            os.path.join('~', 'mcadminpanel')
        ),
        'pidfile': os.path.expanduser(
            os.path.join('~', 'mcadminpanel', 'agent.pid')
        ),
        'logging': {
            'level': 'warn',
            'file': os.path.expanduser(
                os.path.join('~', 'mcadminpanel', 'agent.log')
            ),
            'date_format': '%m-%d-%Y %H:%M:%S',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        }
    }

    def __init__(self, config_file=None):
        """
        Load configuration settings from the specified configuration file
        """

        if config_file is None:
            config_file = Configuration.DEFAULT_CONFIG_FILE

        try:
            with open(config_file, 'r') as config:
                self._config = self._get_config(config)
        except json.JSONDecodeError:
            raise mcadminpanel.agent.errors.ConfigurationError(
                'Unable to parse configuration. Invalid JSON',
            )
        except IOError as ex:
            raise mcadminpanel.agent.errors.ConfigurationError(
                'Unable to open and read configuration file: {}'.format(
                    str(ex)
                ),
            )

    def __getattr__(self, name):
        return self._config.get(name)

    @classmethod
    def save_default_config(cls, path):
        """
        Save a default configuration to the given path
        """

        with open(path, 'w') as file_stream:
            json.dump(cls.DEFAULTS, file_stream, indent=4)

    @classmethod
    def _get_config(cls, raw_config):
        config = json.load(raw_config)

        return merge(cls.DEFAULTS, config)

# pylint: enable=too-few-public-methods

def merge(obj, overrides, clone=True):
    """
    Recursively merge to dictionaries
    """

    result = copy.deepcopy(obj) if clone else obj

    for key, value in overrides.items():
        if key not in result:
            result[key] = value
        elif not isinstance(value, dict) and not isinstance(result[key], dict):
            result[key] = value
        elif isinstance(value, dict) and isinstance(result[key], dict):
            merge(result[key], value, False)

    return result


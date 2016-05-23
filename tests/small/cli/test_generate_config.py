"""
Tests for the CLI generate_config command
"""

import os.path
import unittest
import unittest.mock

from mcadminpanel.agent.cli import mcadminpanel_agent

import tests.utils.mixins

class TestGenConfigCommand(tests.utils.mixins.CliRunnerMixin, unittest.TestCase):
    """
    Tests for the CLI generate_config command
    """

    def setUp(self):
        super(TestGenConfigCommand, self).setUp()

        self.user_home = os.path.expanduser('~')

    def test_is_accessible(self):
        """
        Tests that the command is accessible through normal use
        """

        self._run_test_not_exists(
            os.path.join(self.user_home, 'mcadminpanel'),
            os.path.join(self.user_home, 'mcadminpanel', 'config.json'),
        )

    def test_prompt_dir(self):
        """
        Tests that we use the directory that was given in the prompt
        """

        self._run_test_not_exists(
            'test',
            os.path.join(self.user_home, 'mcadminpanel', 'config.json'),
            user_input='test\n\n\n',
        )

    def test_dir_option(self):
        """
        Tests that we use the directory that was given in the arguments
        """

        self._run_test_not_exists(
            'test',
            os.path.join(self.user_home, 'mcadminpanel', 'config.json'),
            arguments=['--path', 'test'],
        )

    def test_config_prompt(self):
        """
        Tests that we use the configuration path that was given in the prompt
        """

        self._run_test_not_exists(
            os.path.expanduser(os.path.join('~', 'mcadminpanel')),
            'test.json',
            user_input='\ntest.json\n',
        )

    def test_config_option(self):
        """
        Tests that we use the configuraiton path that was given in the arguments
        """

        self._run_test_not_exists(
            os.path.join(self.user_home, 'mcadminpanel'),
            'test.json',
            user_input='\ntest.json\n',
        )

    def test_no_overwrite(self):
        """
        Tests that we don't write a config file if we weren't told to overwrite
        """

        self._run_test_exists(
            os.path.join(self.user_home, 'mcadminpanel'),
            os.path.join(self.user_home, 'mcadminpanel', 'config.json'),
            exit_code=1,
        )

    def _run_test_not_exists(self, path, config, arguments=None, user_input='\n\n\n'):
        if arguments is None:
            arguments = []

        patch = unittest.mock.patch

        with patch('os.makedirs') as makedirs, \
            patch('os.path.exists') as exists, \
            patch('mcadminpanel.agent.config.Configuration') as configuration:
            exists.return_value = False

            configuration.return_value = configuration

            result = self.cli_runner.invoke(
                mcadminpanel_agent,
                ['generate_config'] + arguments,
                input=user_input,
            )

            self.assertEqual(0, result.exit_code, 'Command did not execute properly')

            makedirs.assert_called_with(path, exist_ok=True)

            exists.assert_called_with(config)

            configuration.save_default_config.assert_called_with(config)

    def _run_test_exists(self, path, config, **kwargs):
        arguments = kwargs.get('arguments', [])
        user_input = kwargs.get('user_input', '\n\n\n')
        exit_code = kwargs.get('exit_code', 0)

        patch = unittest.mock.patch

        with patch('os.makedirs') as makedirs, \
            patch('os.path.exists') as exists, \
            patch('mcadminpanel.agent.config.Configuration') as configuration:
            exists.return_value = True

            configuration.return_value = configuration

            result = self.cli_runner.invoke(
                mcadminpanel_agent,
                ['generate_config'] + arguments,
                input=user_input,
            )

            self.assertEqual(
                exit_code,
                result.exit_code,
                'Command did not execute properly',
            )

            makedirs.assert_called_with(path, exist_ok=True)

            exists.assert_called_with(config)

            if exit_code == 0:
                configuration.save_default_config.assert_called_with(config)


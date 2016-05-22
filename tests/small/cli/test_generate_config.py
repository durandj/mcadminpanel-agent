"""
Tests for the CLI generate_config command
"""

import unittest
import unittest.mock

from mcadminpanel.agent.cli import mcadminpanel_agent

import tests.utils.mixins

class TestGenConfigCommand(tests.utils.mixins.CliRunnerMixin, unittest.TestCase):
    """
    Tests for the CLI generate_config command
    """

    @unittest.mock.patch('mcadminpanel.agent.config.Configuration')
    def test_is_accessible(self, configuration):
        """
        Tests that the command is accessible through normal use
        """

        configuration.return_value = configuration

        result = self.cli_runner.invoke(mcadminpanel_agent, ['generate_config'])

        self.assertEqual(0, result.exit_code, 'Command did not execute properly')


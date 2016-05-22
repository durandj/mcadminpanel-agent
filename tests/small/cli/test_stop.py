"""
Tests for the CLI stop command
"""

import unittest
import unittest.mock

from mcadminpanel.agent.cli import mcadminpanel_agent

import tests.utils.mixins

class TestStopCommand(tests.utils.mixins.CliRunnerMixin, unittest.TestCase):
    """
    Tests for the CLI stop command
    """

    @unittest.mock.patch('mcadminpanel.agent.agent.Agent')
    @unittest.mock.patch('mcadminpanel.agent.config.Configuration')
    def test_is_accessible(self, configuration, agent):
        """
        Tests that the command is accessible through normal use
        """

        configuration.return_value = configuration

        agent.return_value = agent

        result = self.cli_runner.invoke(mcadminpanel_agent, ['stop'])

        self.assertEqual(0, result.exit_code, 'Command did not execute properly')

        agent.assert_called_with(configuration)
        agent.stop.assert_called_with()


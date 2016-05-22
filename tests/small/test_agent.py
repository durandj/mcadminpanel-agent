"""
Tests for the agent process
"""

import asyncio
import io
import sys
import tempfile
import unittest
import unittest.mock

import nose

import mcadminpanel.agent.agent
import mcadminpanel.agent.errors

class TestAgent(unittest.TestCase):
    """
    Tests for the agent process
    """

    def setUp(self):
        self.log_file = tempfile.NamedTemporaryFile()

        self.config = unittest.mock.Mock(
            root='myroot',
            pidfile='mypidfile',
            logging={'level': 'warn', 'file': self.log_file.name},
        )

    def test_constr(self):
        """
        Tests that the constructor pulls the correct config values
        """

        agent = mcadminpanel.agent.agent.Agent(self.config)

        self.assertEqual(
            'myroot',
            agent.root,
            'Agent process did not use the correct root directory',
        )

        self.assertEqual(
            'mypidfile',
            agent.pidfile,
            'Agent process did not use the correct PID file',
        )

    @unittest.mock.patch('daemon.pidfile.PIDLockFile')
    @unittest.mock.patch('daemon.DaemonContext')
    def test_start_detach(self, fake_context, fake_pidfile):
        """
        Tests that the agent detaches correctly as a background process
        """

        fake_context.return_value = fake_context

        fake_pidfile.return_value = fake_pidfile

        agent = mcadminpanel.agent.agent.Agent(self.config)
        agent.run = unittest.mock.Mock()

        agent.start(True)

        fake_pidfile.assert_called_with('mypidfile')

        fake_context.assert_called_with(
            detach_process=True,
            working_directory='myroot',
            pidfile=fake_pidfile,
            stdout=None,
            stderr=None,
        )

        agent.run.assert_called_with()

    @unittest.mock.patch('daemon.pidfile.PIDLockFile')
    @unittest.mock.patch('daemon.DaemonContext')
    def test_start_no_detach(self, fake_context, fake_pidfile):
        """
        Tests that the agent detaches correctly as a background process
        """

        fake_context.return_value = fake_context

        fake_pidfile.return_value = fake_pidfile

        agent = mcadminpanel.agent.agent.Agent(self.config)
        agent.run = unittest.mock.Mock()

        agent.start(False)

        fake_pidfile.assert_called_with('mypidfile')

        fake_context.assert_called_with(
            detach_process=False,
            working_directory='myroot',
            pidfile=fake_pidfile,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )

        agent.run.assert_called_with()

    @unittest.mock.patch('psutil.Process')
    @unittest.mock.patch('builtins.open')
    def test_stop(self, fake_open, process):
        """
        Tests that the agent properly stops the process
        """

        fake_open.return_value = fake_open
        fake_open.__enter__.return_value = io.StringIO('007')

        process.return_value = process

        agent = mcadminpanel.agent.agent.Agent(self.config)
        agent.stop()

        fake_open.assert_called_with('mypidfile', 'r')

        process.assert_called_with(7)
        process.terminate.assert_called_with()

    @nose.tools.raises(mcadminpanel.agent.errors.ConfigurationError)
    def test_invalid_log_level(self):
        """
        Tests that we check for a valid log level
        """

        self.config.logging['level'] = 'does_not_exist'

        agent = mcadminpanel.agent.agent.Agent(self.config)
        agent.configure_logger()

    @unittest.mock.patch('asyncio.get_event_loop')
    def test_run_forever(self, get_event_loop):
        """
        Tests that the process runs forever
        """

        event_loop = unittest.mock.MagicMock(
            spec=asyncio.BaseEventLoop,
        )
        get_event_loop.return_value = event_loop

        agent = mcadminpanel.agent.agent.Agent(self.config)
        agent.run()

        get_event_loop.assert_called_with()

        event_loop.run_forever.assert_called_with()


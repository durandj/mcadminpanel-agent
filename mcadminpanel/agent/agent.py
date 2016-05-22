"""
The agent process that manages the servers on this node
"""

import asyncio
import logging
import logging.handlers
import sys

import daemon
import daemon.pidfile
import psutil

import mcadminpanel.agent.errors

class Agent(object):
    """
    Agent process for managing server processes
    """

    def __init__(self, config):
        """
        Setup the agent with the given configuration options
        """

        self.root = config.root
        self.pidfile = config.pidfile
        self.log_conf = config.logging

    def start(self, detach=True):
        """
        Start the agent process and detach
        """

        with daemon.DaemonContext(
            detach_process=detach,
            working_directory=self.root,
            pidfile=daemon.pidfile.PIDLockFile(self.pidfile),
            stdout=(None if detach else sys.stdout),
            stderr=(None if detach else sys.stderr),
        ):
            self.run(detach)

    def stop(self):
        """
        Stop the agent process
        """

        with open(self.pidfile, 'r') as pidfile:
            pid = int(pidfile.read().strip())

        proc = psutil.Process(pid)
        proc.terminate()

    def configure_logger(self, detached):
        """
        Configure the logging system
        """

        log_level = self.log_conf['level'].upper()
        if not hasattr(logging, log_level):
            raise mcadminpanel.agent.errors.ConfigurationError(
                'Improperly configured log level: {}'.format(log_level),
            )
        log_level = getattr(logging, log_level)

        handlers = []

        file_handler = logging.handlers.TimedRotatingFileHandler(
            self.log_conf['file'],
            when='midnight',
        )
        file_handler.setLevel(log_level)
        handlers.append(file_handler)

        if not detached:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(log_level)
            handlers.append(stream_handler)

        logging.basicConfig(
            level=log_level,
            datefmt=self.log_conf['date_format'],
            format=self.log_conf['format'],
            handlers=handlers,
        )

    def run(self, detached):
        """
        The actual agent processing
        """

        self.configure_logger(detached)

        logging.info('Starting agent process...')

        logging.debug('Setting up event loop...')

        event_loop = asyncio.get_event_loop()

        logging.debug('Starting event loop...')

        try:
            event_loop.run_forever()
        finally:
            logging.info('Stopping agent process')

        logging.info('Stopped agent process')


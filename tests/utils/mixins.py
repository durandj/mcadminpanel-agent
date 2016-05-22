"""
Test case mixins
"""

import click.testing

# pylint: disable=invalid-name, too-few-public-methods
class CliRunnerMixin(object):
    """
    TestCase mixin for adding CLI runner to the test environment
    """

    def setUp(self):
        """
        Setup the test CLI runner
        """

        self.cli_runner = click.testing.CliRunner()
# pylint: enable=invalid-name, too-few-public-methods


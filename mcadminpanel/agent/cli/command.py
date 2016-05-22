"""
Main CLI command for the agent
"""

import click

import mcadminpanel.agent.agent
import mcadminpanel.agent.config

@click.group()
@click.option(
    '--config',
    type=click.Path(dir_okay=False, exists=True),
    default=None,
    help='Path to a configuration file')
@click.pass_context
def mcadminpanel_agent(ctx, config):
    """
    MCAdminPanel Agent command for managing the agent process
    """

    ctx.obj = {'config': mcadminpanel.agent.config.Configuration(config)}

@mcadminpanel_agent.command()
def generate_config():
    """
    Generate a config file
    """

# TODO(durandj): implement config command

@mcadminpanel_agent.command()
@click.option(
    '--detach/--no-detach',
    default=True,
    help='Run process in the background')
@click.pass_context
def start(ctx, detach):
    """
    Start the agent
    """

# TODO(durandj): allow passing of config options thru params

    agent = mcadminpanel.agent.agent.Agent(ctx.obj['config'])
    agent.start(detach)

@mcadminpanel_agent.command()
@click.pass_context
def stop(ctx):
    """
    Stop the agent
    """

    agent = mcadminpanel.agent.agent.Agent(ctx.obj['config'])
    agent.stop()


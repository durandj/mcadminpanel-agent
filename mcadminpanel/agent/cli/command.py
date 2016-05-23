"""
Main CLI command for the agent
"""

import os
import os.path

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
@click.option(
    '--path',
    type=click.Path(dir_okay=True),
    prompt=True,
    default=lambda: os.path.expanduser(os.path.join('~', 'mcadminpanel')),
    help='Path where servers will live')
@click.option(
    '--config',
    type=click.Path(file_okay=True),
    prompt=True,
    default=lambda: os.path.expanduser(os.path.join('~', 'mcadminpanel', 'config.json')))
@click.option(
    '--overwrite',
    type=bool,
    default=None,
    help='Overwrite the config file if it exists already')
def generate_config(path, config, overwrite):
    """
    Generate a config file
    """

    os.makedirs(path, exist_ok=True)

    if os.path.exists(config):
        if overwrite is None:
            overwrite = click.confirm('Overwrite existing configuration?')

        if not overwrite:
            raise click.Abort()

        os.remove(config)

    mcadminpanel.agent.config.Configuration.save_default_config(config)

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


"""
MCAdminPanel agent install script
"""

import setuptools

with open('requirements.txt', 'r') as req_file:
    REQUIREMENTS = req_file.readlines()

setuptools.setup(
    name='mcadminpanel-agent',
    version='0.0.1',
    packages=setuptools.find_packages(),
    install_requires=REQUIREMENTS,
    entry_points="""
        [console_scripts]
        mcadminpanel-agent=mcadminpanel.agent.cli:mcadminpanel_agent
    """,
)


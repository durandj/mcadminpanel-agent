"""
Application specific errors and exceptions
"""

class MCAdminPanelError(Exception):
    """
    A generic MCAdminPanel exception
    """

class ConfigurationError(MCAdminPanelError):
    """
    A configuration error in the application
    """


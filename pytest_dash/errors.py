"""Pytest-dash errors."""


class PytestDashError(Exception):
    """Base error for pytest-dash."""


class NoAppFoundError(PytestDashError):
    """No `app` was found in the file."""


class DashAppLoadingError(PytestDashError):
    """The dash app failed to load"""

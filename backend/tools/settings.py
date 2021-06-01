import os
import sys


def e(name, default):
    """Shortcut for os.getnenv."""
    return os.getenv(name, default)


def int_e(name, default):
    """Shortcut for getting int from os.getenv."""
    value = int(e(name, default))
    return value


def float_e(name, default):
    """Shortcut for getting float from os.getenv."""
    value = float(e(name, default))
    return value


def boolean_e(name, default):
    """Shortcut for getting boolean from os.getenv."""
    value = e(name, default)
    return value in {1, "1", "True", "TRUE", "true", True}


def list_e(name, default):
    """Shortcut for getting list from os.getenv."""
    value = e(name, default)
    return value.split(',') if value else []


def is_testing():
    """Check if we are in the testing mode."""
    return (
            'test' in sys.argv
            or 'test_coverage' in sys.argv
            or boolean_e('TESTING', False)
    )

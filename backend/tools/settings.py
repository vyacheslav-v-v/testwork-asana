import os
import sys


def e(name, default):
    """ Shortcut для os.getnenv. """
    return os.getenv(name, default)


def int_e(name, default):
    """ Shortcut для получения int значения из os.getenv. """
    value = int(e(name, default))
    return value


def float_e(name, default):
    """ Shortcut для получения float значения из os.getenv. """
    value = float(e(name, default))
    return value


def boolean_e(name, default):
    """ Shortcut для получения boolean значения из os.getenv. """
    value = e(name, default)
    return value in {1, "1", "True", "TRUE", "true", True}


def list_e(name, default):
    """ Shortcut для получения list значения из os.getenv. """
    value = e(name, default)
    return value.split(',') if value else []


def is_testing():
    """ Проверяет, находимся ли мы в режиме тестирования. """
    return (
            'test' in sys.argv
            or 'test_coverage' in sys.argv
            or boolean_e('TESTING', False)
    )

from importlib import import_module

from fabric.utils import abort


def e(name):
    """
    Set your environment before running other commands
    """
    try:
        import_module('.settings.%s' % name, 'fabfile')
    except ImportError:
        abort('Environment settings not found for "%s"' % name)

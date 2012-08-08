from distutils.core import setup
from twisted.python.dist import getPackages


def refresh_plugin_cache():
    from twisted.plugin import IPlugin, getPlugins
    list(getPlugins(IPlugin))

setup(name='scrivener',
      version='0.1',
      description='Twisted Scribe Client/Server',
      packages=getPackages('scrivener'),
      package_data={'twisted': ['plugins/scribe_tap.py']})

refresh_plugin_cache()

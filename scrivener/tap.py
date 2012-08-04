from twisted.python import usage

from twisted.internet import reactor
from twisted.internet.endpoints import serverFromString
from twisted.python.reflect import namedAny

from scrivener.handlers import TwistedLogHandler
from scrivener.server import ScribeServerService


class Options(usage.Options):
    synopsis = "[scrivener options]"
    optParameters = [
        ["port", "p", "tcp:0",
            "Port to listen on for scribe service."],
        ["handlerFactory", "H", None,
            "Fully Qualified Name of a callable that returns an ILogHandler"]]


def makeService(config):
    endpoint = serverFromString(reactor, config['port'])
    if config['handlerFactory'] is None:
        handlerFactory = TwistedLogHandler
    else:
        handlerFactory = namedAny(config['handlerFactory'])

    return ScribeServerService(endpoint, handlerFactory())

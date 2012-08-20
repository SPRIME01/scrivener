scrivener: A twisted scribe client/server.
==========================================

scrivener is a Scribe_ client/server framework for use with Twisted applications.

Client API
----------

::

    from twisted.internet import reactor
    from twisted.internet.endpoints import TCP4ClientEndpoint
    from scrivener import ScribeClient


    def main():
        client = ScribeClient(TCP4ClientEndpoint(reactor, '127.0.0.1', 1234))
        client.log('category', 'message1')
        client.log('category', 'message2')

    if __name__ == '__main__':
        reactor.callWhenRunning(main)
        reactor.run()


Server API
----------

::

    import sys
    from twisted.internet import reactor
    from twisted.internet.endpoints import TCP4ServerEndpoint
    from twisted.python.log import startLogging

    from scrivener import ScribeServerService
    from scrivener.handlers import TwistedLogHandler


    def main():
        service = ScribeServerService(
            TCP4ServerEndpoint(reactor, 1234),
            TwistedLogHandler())
        service.startService()

    if __name__ == '__main__':
        startLogging(sys.stdout)
        reactor.callWhenRunning(main)
        reactor.run()


Server Plugin
-------------

::
    > twistd -n scrivener --help
    Usage: twistd [options] scrivener [scrivener options]
    Options:
      -p, --port=            Port to listen on for scribe service. [default: tcp:0]
      -H, --handlerFactory=  Fully Qualified Name of a callable that returns an
                             ILogHandler
          --version          Display Twisted version and exit.
          --help             Display this help and exit.

    > twistd -n scrivener -p 1234 -H example.MyLogHandler


.. _Scribe: https://github.com/facebook/scribe
.. _Twisted: http://twistedmatrix.com/

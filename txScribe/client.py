from thrift.transport import TTwisted
from thrift.protocol import TBinaryProtocol

from twisted.python import log

from twisted.internet.protocol import Factory, Protocol
from twisted.internet.defer import Deferred, succeed

from txScribe._thrift.scribe import scribe
from txScribe._thrift.scribe import ttypes


class _NotifyingWrapperProtocol(Protocol):
    def __init__(self, wrapped, on_connectionMade, on_connectionLost):
        self._wrapped = wrapped
        self._on_connectionMade = on_connectionMade
        self._on_connectionLost = on_connectionLost

    def dataReceived(self, data):
        self._wrapped.dataReceived(data)

    def connectionMade(self):
        self._wrapped.makeConnection(self.transport)
        self._on_connectionMade(self._wrapped)

    def connectionLost(self, reason):
        self._wrapped.connectionLost(reason)
        self._on_connectionLost(reason)


class _ThriftClientFactory(Factory):
    def __init__(self, client_class, on_connectionMade, on_connectionLost):
        self._client_class = client_class
        self._on_connectionMade = on_connectionMade
        self._on_connectionLost = on_connectionLost

    def buildProtocol(self, addr):
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()
        p = TTwisted.ThriftClientProtocol(self._client_class, pfactory)

        wrapper = _NotifyingWrapperProtocol(
            p, self._on_connectionMade, self._on_connectionLost)

        return wrapper


class ScribeClient(object):
    _NOT_CONNECTED = 0
    _CONNECTING = 1
    _CONNECTED = 2

    _state = _NOT_CONNECTED

    def __init__(self, scribe_endpoint):
        self._scribe_endpoint = scribe_endpoint
        self._client_factory = _ThriftClientFactory(
            scribe.Client,
            self._connection_made,
            self._connection_lost)
        self._client = None
        self._waiting = []

    def _notify_connected(self):
        d = Deferred()
        self._waiting.append(d)
        return d

    def _connection_made(self, client):
        self._client = client
        self.state = self._CONNECTED
        while self._waiting:
            d = self._waiting.pop(0)
            d.callback(self._client)

    def _connection_lost(self, reason):
        self.state = self._NOT_CONNECTED
        log.err(
            reason,
            "Connection lost to scribe server: {0}".format(self._scribe_endpoint))

    def _connection_failed(self, reason):
        self.state = self._NOT_CONNECTED
        log.err(
            reason,
            "Could not connect to scribe server: {0}".format(self._scribe_endpoint))

    def _get_client(self):
        if self.state == self._NOT_CONNECTED:
            self.state = self._CONNECTING
            nd = self._notify_connected()
            d = self._scribe_endpoint.connect(self._client_factory)
            d.addErrback(self._connection_failed)
            d.addCallback(lambda _: nd)
            return d
        elif self.state == self._CONNECTING:
            return self._notify_connected()
        elif self.state == self._CONNECTED:
            return succeed(self._client)

    def log(self, category, messages):
        entries = [ttypes.LogEntry(category, message) for message in messages]

        def _log(client):
            return client.client.Log(entries)

        d = self._get_client()
        d.addCallback(_log)
        return d

